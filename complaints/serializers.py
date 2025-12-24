from rest_framework import serializers
from .models import Complaint, Ward, Verification, UserProfile, ComplaintImage

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['id', 'name', 'officer_email', 'full_name']

class ComplaintSerializer(serializers.ModelSerializer):
    # 1. Magic Trick: Send the Ward's NAME (e.g. "G/North") instead of just ID "1"
    ward_name = serializers.CharField(source='ward.name', read_only=True)
    
    # 2. Dynamic Field: Count how many upvotes this has
    verification_count = serializers.SerializerMethodField()
    
    # 3. Dynamic Field: Check if current user has verified
    is_verified = serializers.SerializerMethodField()

    # 4. Reporter Info
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)

    class Meta:
        model = Complaint
        fields = [
            'id', 'title', 'description', 'category', 'status', 
            'latitude', 'longitude', 'location_address', 
            'ward', 'ward_name', 
            'image', 'urgency_score', 'verification_count', 'is_verified', 
            'reporter', 'reporter_username', 'is_anonymous', 'created_at'
        ]
        # Security: Users shouldn't be able to manually change these via API
        read_only_fields = ['urgency_score', 'status', 'created_at']

    def validate(self, data):
        """
        Restrict complaints to Mumbai region only.
        """
        lat = data.get('latitude')
        lng = data.get('longitude')

        if lat and lng:
            # Mumbai Bounds (Approximate)
            # South: 18.89, North: 19.30
            # West: 72.75, East: 73.00
            if not (18.89 <= float(lat) <= 19.30 and 72.75 <= float(lng) <= 73.00):
                raise serializers.ValidationError({
                    "location": "Jan Sevak is currently available only in Mumbai. Please select a location within the city."
                })
        
        return data

    def get_verification_count(self, obj):
        # This asks the database: "Count all verification rows linked to this complaint"
        return obj.verifications.count()

    def get_is_verified(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            return obj.verifications.filter(user=user).exists()
        return False

class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['id', 'image', 'uploaded_at']

class ComplaintSerializer(serializers.ModelSerializer):
    # 1. Magic Trick: Send the Ward's NAME (e.g. "G/North") instead of just ID "1"
    ward_name = serializers.CharField(source='ward.name', read_only=True)
    
    # 2. Dynamic Field: Count how many upvotes this has
    verification_count = serializers.SerializerMethodField()
    
    # 3. Dynamic Field: Check if current user has verified
    is_verified = serializers.SerializerMethodField()

    # 4. Reporter Info
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)

    # 5. Multiple Images
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    uploaded_images = ComplaintImageSerializer(source='images', many=True, read_only=True)

    class Meta:
        model = Complaint
        fields = [
            'id', 'title', 'description', 'category', 'status', 
            'latitude', 'longitude', 'location_address', 
            'ward', 'ward_name', 
            'image', 'images', 'uploaded_images', # Added images fields
            'urgency_score', 'verification_count', 'is_verified', 
            'reporter', 'reporter_username', 'is_anonymous', 'created_at',
            'cc_reporter'
        ]
        # Security: Users shouldn't be able to manually change these via API
        read_only_fields = ['urgency_score', 'status', 'created_at']

    def validate(self, data):
        """
        Restrict complaints to Mumbai region only.
        """
        lat = data.get('latitude')
        lng = data.get('longitude')

        if lat and lng:
            # Mumbai Bounds (Approximate)
            # South: 18.89, North: 19.30
            # West: 72.75, East: 73.00
            if not (18.89 <= float(lat) <= 19.30 and 72.75 <= float(lng) <= 73.00):
                raise serializers.ValidationError({
                    "location": "Jan Sevak is currently available only in Mumbai. Please select a location within the city."
                })
        
        # Mandatory Image Validation
        images = data.get('images', [])
        legacy_image = data.get('image')
        
        if not images and not legacy_image:
             raise serializers.ValidationError({
                "images": "At least one photo is required to report an issue."
            })

        return data

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        complaint = Complaint.objects.create(**validated_data)
        
        # Handle multiple images
        for image_data in images_data:
            ComplaintImage.objects.create(complaint=complaint, image=image_data)
            
        return complaint

    def get_verification_count(self, obj):
        # This asks the database: "Count all verification rows linked to this complaint"
        return obj.verifications.count()

    def get_is_verified(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            return obj.verifications.filter(user=user).exists()
        return False

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['username', 'points', 'badges']