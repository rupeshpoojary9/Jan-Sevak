from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Complaint, Ward, Verification
from .serializers import ComplaintSerializer, WardSerializer
class WardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows wards to be viewed.
    """
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    pagination_class = None

class ComplaintViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows complaints to be viewed or edited.
    """
    # OPTIMIZATION:
    # 1. select_related('ward'): Performs a SQL JOIN to fetch Ward data in the same query.
    #    Without this, Django would run a separate query for every complaint to get the ward name.
    # 2. prefetch_related('verifications'): Efficiently fetches the upvotes in a second query.
    # 3. order_by('-created_at'): Ensures the newest complaints show up first.
    queryset = Complaint.objects.select_related('ward').prefetch_related('verifications').all().order_by('-created_at')
    
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Authentication is handled by DEFAULT_AUTHENTICATION_CLASSES in settings.py
    # which includes both JWTCookieAuthentication (for browser) and JWTAuthentication (for API)
    
    # Add Search and Filter Capability
    from rest_framework import filters
    from django_filters.rest_framework import DjangoFilterBackend
    from .filters import ComplaintFilter
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'ward__name', 'ward__full_name']
    filterset_class = ComplaintFilter

    # Custom Action: Verify (Upvote) a Complaint
    # URL will be: POST /api/complaints/{id}/verify/
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        complaint = self.get_object()
        
        # 1. Check if user is logged in (Anonymous users can't vote in this version)
        if not request.user.is_authenticated:
             return Response({'error': 'Please login to verify.'}, status=status.HTTP_401_UNAUTHORIZED)

        # 2. Check if user is reporter
        if request.user == complaint.reporter:
             return Response({'message': 'You cannot verify your own complaint.'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Check if already verified
        if Verification.objects.filter(complaint=complaint, user=request.user).exists():
            return Response({'message': 'You have already verified this issue.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. Add Verification
        Verification.objects.create(complaint=complaint, user=request.user)
        
        return Response({
            'status': 'verified', 
            'total_verifications': complaint.verifications.count()
        })

    # Custom Action: Get User's Complaints (Dashboard)
    # URL: GET /api/complaints/my_complaints/
    @action(detail=False, methods=['get'])
    def my_complaints(self, request):
        if not request.user.is_authenticated:
             return Response({'error': 'Please login to view your dashboard.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Filter complaints by the current user
        # We use self.queryset to keep the select_related/prefetch_related optimizations
        my_complaints = self.queryset.filter(reporter=request.user)
        
        # Apply Pagination
        page = self.paginate_queryset(my_complaints)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_complaints, many=True)
        return Response(serializer.data)

    # Custom Action: Get GeoJSON Data for Map
    # URL: GET /api/complaints/geojson/
    @action(detail=False, methods=['get'])
    def geojson(self, request):
        # Fetch all complaints (optimize query)
        # Fetch all complaints (optimize query)
        complaints = Complaint.objects.select_related('ward').all()
        
        features = []
        for c in complaints:
            # Skip if coordinates are missing
            if c.latitude is None or c.longitude is None:
                continue
                
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [c.longitude, c.latitude] # GeoJSON is [lon, lat]
                },
                "properties": {
                    "id": c.id,
                    "title": c.title,
                    "category": c.category,
                    "status": c.status,
                    "urgency_score": c.urgency_score,
                    "ward_name": c.ward.name if c.ward else "Unknown",
                    "image": c.image.url if c.image else None
                }
            })
        
        data = {
            "type": "FeatureCollection",
            "features": features
        }
        data = {
            "type": "FeatureCollection",
            "features": features
        }
        return Response(data)

    # Custom Action: User Confirms Resolution
    # URL: POST /api/complaints/{id}/confirm_resolution/
    @action(detail=True, methods=['post'])
    def confirm_resolution(self, request, pk=None):
        complaint = self.get_object()
        
        # Only the reporter can confirm
        if complaint.reporter != request.user:
             return Response({'error': 'Only the reporter can confirm this.'}, status=status.HTTP_403_FORBIDDEN)
             
        complaint.user_confirmed = True
        complaint.save()
        
        return Response({'status': 'confirmed'})

    def perform_create(self, serializer):
        # Save the complaint first to get the image path
        complaint = serializer.save(reporter=self.request.user if self.request.user.is_authenticated else None)
        
        # Trigger AI Analysis (Synchronous for Moderation)
        # We analyze description even if no image is present
        from .ai_service import analyze_complaint
        from rest_framework.exceptions import ValidationError
        import os
        
        image_path = complaint.image.path if complaint.image else None
        
        # Call AI
        is_valid, reason, score, verified = analyze_complaint(image_path, complaint.description, complaint.category)
            
        if not is_valid:
            # Delete the invalid complaint and file
            if complaint.image:
                image_path = complaint.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            complaint.delete()
            raise ValidationError({"error": f"Complaint rejected by AI: {reason}"})
        
        # If valid, update scores
        complaint.urgency_score = score
        complaint.ai_verified_category = verified
        complaint.ai_verified_category = verified
        complaint.save()

    def perform_destroy(self, instance):
        # Check ownership
        if instance.reporter != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own complaints.")

        # Allow deletion only if status is NEW
        if instance.status != Complaint.Status.NEW:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You can only delete complaints that are 'New'. Processed complaints cannot be deleted.")
        
        # Delete the image file if it exists
        if instance.image:
            import os
            if os.path.exists(instance.image.path):
                os.remove(instance.image.path)
                
        instance.delete()

from .models import UserProfile
from .serializers import UserProfileSerializer

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for the Leaderboard.
    """
    queryset = UserProfile.objects.all().order_by('-points')[:10]
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_profile(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Magic Link View (No Authentication Required)
def resolve_complaint(request, pk, token):
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Security Check: Verify Token
    if str(complaint.admin_token) != str(token):
        return HttpResponse("Invalid Token", status=403)
    
    # Mark as Resolved
    complaint.status = Complaint.Status.RESOLVED
    complaint.save()
    
    # Award Points (Trigger Signal) - This happens automatically via post_save signal
    
    return HttpResponse(f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1 style="color: green;">Complaint Resolved!</h1>
            <p>Thank you for taking action on Complaint #{pk}.</p>
            <p>The citizen has been notified.</p>
        </body>
    </html>
    """)