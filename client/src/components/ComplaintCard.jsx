import React, { useState } from 'react';
import axios from 'axios';

import { useAuth } from '../context/AuthContext';
import { getMediaUrl } from '../utils/media';

// 1. PROPS: We receive 'complaint' data and an 'onVerify' function from the parent.
// This makes the component reusable for ANY complaint.
const ComplaintCard = ({ complaint, onDelete }) => {
    const { user } = useAuth();
    const [verifications, setVerifications] = useState(complaint.verification_count);
    const [isConfirmed, setIsConfirmed] = useState(complaint.user_confirmed);
    const [hasVerified, setHasVerified] = useState(complaint.is_verified || false); // Initialize from backend prop

    const handleVerify = async () => {
        // Optimistic Update: Assume success and update UI immediately
        setVerifications(prev => prev + 1);
        setHasVerified(true);

        try {
            const res = await axios.post(`/api/complaints/${complaint.id}/verify/`);
            // Sync with actual server count (should be the same)
            setVerifications(res.data.total_verifications);
        } catch (err) {
            // Revert on failure
            setVerifications(prev => prev - 1);
            setHasVerified(false);

            // If already verified, backend might return 400
            if (err.response && err.response.status === 400) {
                const msg = err.response.data?.message;

                if (msg === 'You have already verified this issue.') {
                    setHasVerified(true);
                    setVerifications(prev => prev + 1); // Re-add because it WAS verified
                    alert("You have already verified this issue.");
                } else {
                    // Other 400 errors (like own complaint)
                    alert(msg || "Failed to verify");
                }
            } else {
                alert(err.response?.data?.message || "Failed to verify");
            }
        }
    };

    const handleConfirm = async () => {
        try {
            await axios.post(`/api/complaints/${complaint.id}/confirm_resolution/`);
            setIsConfirmed(true);
        } catch (err) {
            alert(err.response?.data?.error || "Failed to confirm");
        }
    };

    // Helper to choose color based on urgency
    const getUrgencyColor = (score) => {
        if (score >= 8) return 'bg-red-100 text-red-800 border-red-200'; // Critical
        if (score >= 5) return 'bg-yellow-100 text-yellow-800 border-yellow-200'; // Moderate
        return 'bg-green-100 text-green-800 border-green-200'; // Low
    };

    const handleShare = async () => {
        const shareData = {
            title: `Jan Sevak: ${complaint.title}`,
            text: `Check out this civic issue reported on Jan Sevak: ${complaint.title}`,
            url: window.location.href
        };

        if (navigator.share) {
            try {
                await navigator.share(shareData);
            } catch (err) {
                console.log('Error sharing', err);
            }
        } else {
            // Fallback to clipboard
            navigator.clipboard.writeText(`${shareData.text} ${shareData.url}`);
            alert("Link copied to clipboard!");
        }
    };

    const getStatusBadge = (status) => {
        const styles = {
            'NEW': 'bg-blue-100 text-blue-800',
            'VERIFIED': 'bg-purple-100 text-purple-800',
            'IN_PROGRESS': 'bg-yellow-100 text-yellow-800',
            'RESOLVED': 'bg-green-100 text-green-800',
            'REJECTED': 'bg-red-100 text-red-800'
        };
        return (
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide ${styles[status] || 'bg-gray-100 text-gray-800'}`}>
                {status.replace('_', ' ')}
            </span>
        );
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);

        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
        return `${Math.floor(diffInSeconds / 86400)}d ago`;
    };

    const [currentImageIndex, setCurrentImageIndex] = useState(0);



    // Combine legacy image and new multiple images
    const images = complaint.uploaded_images && complaint.uploaded_images.length > 0
        ? complaint.uploaded_images.map(img => getMediaUrl(img.image))
        : (complaint.image ? [getMediaUrl(complaint.image)] : []);

    const nextImage = (e) => {
        e.stopPropagation();
        setCurrentImageIndex((prev) => (prev + 1) % images.length);
    };

    const prevImage = (e) => {
        e.stopPropagation();
        setCurrentImageIndex((prev) => (prev - 1 + images.length) % images.length);
    };

    return (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden card-hover group flex flex-col h-full">

            {/* Image Section */}
            {images.length > 0 && (
                <div className="h-56 overflow-hidden relative group/image">
                    <img
                        src={images[currentImageIndex]}
                        alt={complaint.title}
                        className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
                    />

                    {/* Carousel Controls */}
                    {images.length > 1 && (
                        <>
                            <button
                                onClick={prevImage}
                                className="absolute left-2 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-1 rounded-full opacity-0 group-hover/image:opacity-100 transition-opacity"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                                </svg>
                            </button>
                            <button
                                onClick={nextImage}
                                className="absolute right-2 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-1 rounded-full opacity-0 group-hover/image:opacity-100 transition-opacity"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                                </svg>
                            </button>

                            {/* Dots Indicator */}
                            <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex space-x-1">
                                {images.map((_, idx) => (
                                    <div
                                        key={idx}
                                        className={`h-1.5 w-1.5 rounded-full ${idx === currentImageIndex ? 'bg-white' : 'bg-white/50'}`}
                                    />
                                ))}
                            </div>
                        </>
                    )}

                    <div className="absolute top-3 right-3 flex space-x-2">
                        <span className={`px-3 py-1 rounded-full text-xs font-bold shadow-sm backdrop-blur-md ${getUrgencyColor(complaint.urgency_score)}`}>
                            Urgency {complaint.urgency_score}/10
                        </span>
                    </div>
                </div>
            )}

            {/* Content Section */}
            <div className="p-6 flex-1 flex flex-col">
                <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center space-x-2 text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                        </svg>
                        <span>{complaint.ward_name} • {complaint.category}</span>
                    </div>
                    <div className="flex items-center gap-2">
                        {complaint.urgency_score > 0 && (
                            <span className={`px-2 py-0.5 rounded-full text-xs font-bold border ${getUrgencyColor(complaint.urgency_score)}`}>
                                Urgency {complaint.urgency_score}/10
                            </span>
                        )}
                        {getStatusBadge(complaint.status)}
                    </div>
                </div>

                <h3 className="text-xl font-heading font-bold text-gray-900 mb-2 leading-tight">{complaint.title}</h3>
                <p className="text-gray-600 text-sm mb-4 line-clamp-3 leading-relaxed flex-1">{complaint.description}</p>

                {/* Meta Info */}
                <div className="flex items-center justify-between text-xs text-gray-400 mb-4 pt-4 border-t border-gray-50">
                    <div className="flex items-center space-x-1">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        <span>{complaint.is_anonymous ? 'Anonymous' : (complaint.reporter_username || 'Citizen Reporter')}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span>{formatDate(complaint.created_at)}</span>
                    </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center justify-between">
                    <button
                        onClick={handleVerify}
                        disabled={hasVerified || (user && (user.pk === complaint.reporter || user.id === complaint.reporter))}
                        className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${hasVerified || (user && (user.pk === complaint.reporter || user.id === complaint.reporter))
                            ? 'bg-green-50 text-green-700 border border-green-200 cursor-default opacity-70'
                            : 'bg-gray-50 text-gray-600 hover:bg-blue-50 hover:text-blue-600'
                            }`}
                    >
                        {hasVerified ? (
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                        ) : (
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                        )}
                        <span>
                            {user && (user.pk === complaint.reporter || user.id === complaint.reporter)
                                ? 'Own Complaint'
                                : (hasVerified ? 'Verified' : 'Verify')}
                        </span>
                        <span className={`ml-1 text-xs font-bold px-2 py-0.5 rounded-full ${hasVerified ? 'bg-green-200 text-green-800' : 'bg-gray-200 text-gray-700'}`}>
                            {verifications}
                        </span>
                    </button>

                    <button
                        onClick={handleShare}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
                        title="Share"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                        </svg>
                    </button>

                    {/* Delete Button (Only for Owner & NEW status) */}
                    {onDelete && user && (user.pk === complaint.reporter || user.id === complaint.reporter) && complaint.status === 'NEW' && (
                        <button
                            onClick={() => {
                                if (window.confirm('Are you sure you want to delete this complaint?')) {
                                    onDelete(complaint.id);
                                }
                            }}
                            className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors ml-2"
                            title="Delete"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ComplaintCard;
