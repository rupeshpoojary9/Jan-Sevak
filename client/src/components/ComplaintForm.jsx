import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';

const ComplaintForm = ({ onSuccess }) => {
    const { t } = useTranslation();
    const [wards, setWards] = useState([]);
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        category: 'OTHERS',
        ward: '',
        image: null,
        location_address: '',
        is_anonymous: false
    });
    const [loading, setLoading] = useState(false);
    const [analyzing, setAnalyzing] = useState(false);
    const [location, setLocation] = useState(null);
    const [locationStatus, setLocationStatus] = useState('idle'); // idle, loading, success, error
    const [preview, setPreview] = useState(null);
    const fileInputRef = useRef(null);

    // Fetch Wards on mount
    useEffect(() => {
        axios.get('/api/wards/')
            .then(res => setWards(res.data))
            .catch(err => console.error("Failed to fetch wards", err));
    }, []);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFormData(prev => ({ ...prev, image: file }));
            setPreview(URL.createObjectURL(file));
        }
    };

    const handleGetLocation = () => {
        if (!navigator.geolocation) {
            setLocationStatus('error');
            alert('Geolocation is not supported by your browser');
            return;
        }

        setLocationStatus('loading');
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                setLocation({ latitude: lat, longitude: lng });
                setLocationStatus('success');

                // Auto-fill address with coordinates if empty
                if (!formData.location_address) {
                    setFormData(prev => ({
                        ...prev,
                        location_address: `Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)}`
                    }));
                }
            },
            (error) => {
                console.error("Error getting location:", error);
                setLocationStatus('error');
                alert('Unable to retrieve your location. Please enable location services.');
            }
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // 1. Validation: Title Length
        if (formData.title.length < 10) {
            alert("Title is too short. Please provide at least 10 characters.");
            return;
        }

        // 2. Validation: Description Length
        if (formData.description.length < 50) {
            alert("Description is too short. Please explain the issue in detail (at least 50 characters).");
            return;
        }

        // TEST MODE: Allow submission without GPS (Random Mumbai Location)
        let finalLocation = location;
        if (!finalLocation) {
            // Generate random coordinates around Mumbai
            const baseLat = 19.0760;
            const baseLng = 72.8777;
            const randomLat = baseLat + (Math.random() - 0.5) * 0.1; // +/- 0.05 degrees
            const randomLng = baseLng + (Math.random() - 0.5) * 0.1;

            finalLocation = { latitude: randomLat, longitude: randomLng };

            alert("⚠️ TEST MODE: No GPS detected. Assigning a RANDOM location in Mumbai for testing purposes.");
        }

        setLoading(true);
        setAnalyzing(true);

        // Create FormData object for file upload
        const data = new FormData();
        data.append('title', formData.title);
        data.append('description', formData.description);
        data.append('category', formData.category);
        data.append('ward', formData.ward);
        data.append('latitude', finalLocation.latitude);
        data.append('longitude', finalLocation.longitude);
        data.append('location_address', formData.location_address);
        data.append('is_anonymous', formData.is_anonymous);

        if (formData.image) {
            data.append('image', formData.image);
        }

        try {
            await axios.post('/api/complaints/', data, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            alert("Complaint Verified & Submitted Successfully!");
            if (onSuccess) onSuccess(); // Callback to refresh the list

            // Reset form
            setFormData({
                title: '', description: '', category: 'OTHERS', ward: '',
                image: null, location_address: '', is_anonymous: false
            });
            setPreview(null);
            setLocation(null);
            setLocationStatus('idle');
        } catch (err) {
            console.error("Submission Error:", err);
            let errorMessage = "Error submitting complaint.";

            if (err.response?.data) {
                const data = err.response.data;
                if (data.error) {
                    errorMessage = Array.isArray(data.error) ? data.error[0] : data.error;
                } else if (data.detail) {
                    errorMessage = data.detail;
                } else {
                    const firstField = Object.keys(data)[0];
                    const firstError = Array.isArray(data[firstField]) ? data[firstField][0] : data[firstField];
                    errorMessage = `${firstField}: ${firstError}`;
                }
            } else if (err.message) {
                errorMessage = err.message;
            }

            alert("❌ Submission Failed:\n" + errorMessage);
        } finally {
            setLoading(false);
            setAnalyzing(false);
        }
    };

    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
            <h2 className="text-2xl font-heading font-bold mb-6 text-gray-900 border-b border-gray-100 pb-4">{t('complaint_form.title')}</h2>
            <form onSubmit={handleSubmit} className="space-y-6">

                {/* Section 1: Issue Details */}
                <div className="space-y-4">
                    <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider">1. Issue Details</h3>

                    {/* Image Upload */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('complaint_form.upload_image')}</label>
                        <div className="flex items-center justify-center w-full">
                            <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
                                {preview ? (
                                    <img src={preview} alt="Preview" className="w-full h-full object-contain rounded-lg" />
                                ) : (
                                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                        <svg className="w-8 h-8 mb-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
                                        </svg>
                                        <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                                        <p className="text-xs text-gray-500">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
                                    </div>
                                )}
                                <input ref={fileInputRef} type="file" className="hidden" onChange={handleImageChange} accept="image/*" />
                            </label>
                        </div>
                    </div>

                    {/* Title */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                        <input
                            type="text"
                            name="title"
                            value={formData.title}
                            onChange={handleChange}
                            required
                            minLength={10}
                            className="input-field"
                            placeholder="e.g. Large Pothole near Station"
                        />
                        <p className="text-xs text-gray-400 mt-1 text-right">{formData.title.length}/10 chars</p>
                    </div>

                    {/* Description */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">{t('complaint_form.description')}</label>
                        <textarea
                            name="description"
                            value={formData.description}
                            onChange={handleChange}
                            required
                            minLength={50}
                            rows="3"
                            className="input-field"
                            placeholder="Describe the issue in detail..."
                        />
                        <p className="text-xs text-gray-400 mt-1 text-right">{formData.description.length}/50 chars</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Category */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">{t('complaint_form.category')}</label>
                            <select
                                name="category"
                                value={formData.category}
                                onChange={handleChange}
                                className="input-field"
                            >
                                <option value="POTHOLE">Pothole</option>
                                <option value="GARBAGE">Garbage</option>
                                <option value="DRAINAGE">Drainage</option>
                                <option value="LIGHTING">Street Lights</option>
                                <option value="WATER">Water Supply</option>
                                <option value="SANITATION">Public Toilets/Sanitation</option>
                                <option value="TRAFFIC">Traffic/Parking</option>
                                <option value="PARKS">Parks/Gardens</option>
                                <option value="OTHERS">Others</option>
                            </select>
                        </div>

                        {/* Ward */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Ward</label>
                            <select
                                name="ward"
                                value={formData.ward}
                                onChange={handleChange}
                                required
                                className="input-field"
                            >
                                <option value="">Select Ward</option>
                                {wards.map(ward => (
                                    <option key={ward.id} value={ward.id}>{ward.name} - {ward.full_name}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>

                {/* Section 2: Location */}
                <div className="space-y-4 pt-4 border-t border-gray-50">
                    <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider">2. Location</h3>

                    <div>
                        <div className="flex flex-col space-y-2">
                            <button
                                type="button"
                                onClick={handleGetLocation}
                                disabled={locationStatus === 'loading'}
                                className={`w-full py-3 px-4 rounded-xl border-2 font-medium transition-all flex items-center justify-center space-x-2
                                ${locationStatus === 'success'
                                        ? 'border-green-500 text-green-700 bg-green-50'
                                        : 'border-gray-200 text-gray-600 hover:border-blue-500 hover:text-blue-600'
                                    }`}
                            >
                                {locationStatus === 'loading' ? (
                                    <>
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
                                        <span>Locating...</span>
                                    </>
                                ) : locationStatus === 'success' ? (
                                    <>
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                            <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                                        </svg>
                                        <span>Location Tagged</span>
                                    </>
                                ) : (
                                    <>
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                        </svg>
                                        <span>Get GPS Location</span>
                                    </>
                                )}
                            </button>
                            <p className="text-xs text-center text-gray-400">
                                (Test Mode: You can skip this to use a random location)
                            </p>
                        </div>
                        {locationStatus === 'error' && (
                            <p className="mt-1 text-sm text-red-600">Could not fetch location. Please try again.</p>
                        )}
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">{t('complaint_form.location')}</label>
                        <input
                            type="text"
                            name="location_address"
                            value={formData.location_address}
                            onChange={handleChange}
                            className="input-field"
                            placeholder="Landmark or Address"
                        />
                    </div>
                </div>

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={loading}
                    className={`w-full py-3 px-4 rounded-lg text-white font-medium text-lg shadow-lg transition-all transform hover:-translate-y-0.5 ${loading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 shadow-blue-500/30'
                        }`}
                >
                    {loading ? (
                        <span className="flex items-center justify-center gap-2">
                            <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            {analyzing ? t('complaint_form.analyzing') : t('common.loading')}
                        </span>
                    ) : (
                        t('complaint_form.submit')
                    )}
                </button>
            </form>
        </div>
    );
};

export default ComplaintForm;
