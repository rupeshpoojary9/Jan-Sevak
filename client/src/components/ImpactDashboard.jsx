import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';

const ImpactDashboard = () => {
    const { t } = useTranslation();
    const [stats, setStats] = useState({
        total_complaints: 0,
        resolved_complaints: 0,
        total_users: 0,
        impact_score: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await axios.get('/api/public-stats/');
                setStats(response.data);
            } catch (error) {
                console.error("Failed to fetch public stats", error);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    if (loading) return null;

    return (
        <div className="bg-white py-12 sm:py-16">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-2xl lg:max-w-none">
                    <div className="text-center">
                        <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                            Real Impact, Real Time 🚀
                        </h2>
                        <p className="mt-4 text-lg leading-8 text-gray-600">
                            See how Jan Sevak is transforming our city, one complaint at a time.
                        </p>
                    </div>
                    <dl className="mt-16 grid grid-cols-1 gap-0.5 overflow-hidden rounded-2xl text-center sm:grid-cols-2 lg:grid-cols-4">
                        <div className="flex flex-col bg-gray-400/5 p-8">
                            <dt className="text-sm font-semibold leading-6 text-gray-600">Total Issues Reported</dt>
                            <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900">{stats.total_complaints}</dd>
                        </div>
                        <div className="flex flex-col bg-gray-400/5 p-8">
                            <dt className="text-sm font-semibold leading-6 text-gray-600">Issues Resolved</dt>
                            <dd className="order-first text-3xl font-semibold tracking-tight text-green-600">{stats.resolved_complaints}</dd>
                        </div>
                        <div className="flex flex-col bg-gray-400/5 p-8">
                            <dt className="text-sm font-semibold leading-6 text-gray-600">Active Citizens</dt>
                            <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900">{stats.total_users}</dd>
                        </div>
                        <div className="flex flex-col bg-gray-400/5 p-8">
                            <dt className="text-sm font-semibold leading-6 text-gray-600">Community Impact Score</dt>
                            <dd className="order-first text-3xl font-semibold tracking-tight text-blue-600">{stats.impact_score}</dd>
                        </div>
                    </dl>
                </div>
            </div>
        </div>
    );
};

export default ImpactDashboard;
