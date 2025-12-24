import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import ComplaintCard from '../components/ComplaintCard';
import { useTranslation } from 'react-i18next';
import { useComplaint } from '../context/ComplaintContext';

const DashboardPage = () => {
    const { user } = useAuth();
    const { t } = useTranslation();
    const { complaintUpdateTrigger } = useComplaint();
    const [myComplaints, setMyComplaints] = useState([]);
    const [stats, setStats] = useState({ total: 0, resolved: 0, pending: 0 });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMyComplaints = async () => {
            try {
                const response = await axios.get('/api/complaints/my_complaints/');
                // Handle pagination (Django Rest Framework returns { results: [...] } for paginated responses)
                const data = response.data.results ? response.data.results : (Array.isArray(response.data) ? response.data : []);

                if (!Array.isArray(data)) {
                    console.warn('Expected array of complaints but got:', response.data);
                    setMyComplaints([]);
                } else {
                    setMyComplaints(data);
                }

                // Calculate stats
                const total = data.length;
                const resolved = data.filter(c => c.status === 'RESOLVED').length;
                const pending = total - resolved;
                setStats({ total, resolved, pending });
            } catch (error) {
                console.error("Failed to fetch complaints", error);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            fetchMyComplaints();
        }
    }, [user, complaintUpdateTrigger]);

    const handleDelete = (deletedId) => {
        setMyComplaints(prev => prev.filter(c => c.id !== deletedId));
        // Update stats locally
        setStats(prev => ({
            ...prev,
            total: prev.total - 1,
            pending: prev.pending - 1 // Assuming deleted was pending, simplified logic
        }));
    };

    if (loading) return <div className="p-8 text-center">{t('common.loading')}</div>;

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">{t('dashboard.welcome')}, {user?.username}!</h1>
                <p className="mt-2 text-gray-600">{t('dashboard.track_issues')}</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="text-sm font-medium text-gray-500 uppercase">{t('dashboard.total_reported')}</div>
                    <div className="mt-2 text-3xl font-bold text-gray-900">{stats.total}</div>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="text-sm font-medium text-gray-500 uppercase">{t('dashboard.resolved')}</div>
                    <div className="mt-2 text-3xl font-bold text-green-600">{stats.resolved}</div>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="text-sm font-medium text-gray-500 uppercase">{t('dashboard.pending')}</div>
                    <div className="mt-2 text-3xl font-bold text-orange-600">{stats.pending}</div>
                </div>
            </div>

            {/* My Complaints List */}
            <div>
                <h2 className="text-xl font-bold text-gray-900 mb-4">{t('dashboard.my_complaints')}</h2>
                {myComplaints.length === 0 ? (
                    <div className="text-center py-12 bg-white rounded-xl border border-dashed border-gray-300">
                        <p className="text-gray-500">{t('dashboard.no_complaints')}</p>
                    </div>
                ) : (
                    <div className="space-y-6">
                        {myComplaints.map(complaint => (
                            <ComplaintCard key={complaint.id} complaint={complaint} onDelete={handleDelete} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default DashboardPage;
