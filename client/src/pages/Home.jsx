import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';
import { useComplaint } from '../context/ComplaintContext';
import Navbar from '../components/Navbar';
import ComplaintList from '../components/ComplaintList';
import Footer from '../components/Footer';
import LandingPage from './LandingPage';

const Home = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    console.log("Rendering Home Component");
    const { t } = useTranslation();
    const { complaintUpdateTrigger } = useComplaint();
    const [refreshKey, setRefreshKey] = useState(0);

    // Update refresh key when global trigger changes
    useEffect(() => {
        setRefreshKey(prev => prev + 1);
    }, [complaintUpdateTrigger]);

    // If not authenticated, show Landing Page
    if (!user) {
        return (
            <div className="min-h-screen bg-gray-50 flex flex-col">
                <Navbar />
                <main className="flex-grow">
                    <LandingPage />
                </main>
                <Footer />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            <Navbar />

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
                <div className="mb-6">
                    <h1 className="text-2xl font-bold text-gray-900">{t('navbar.home')}</h1>
                </div>

                <ComplaintList key={refreshKey} endpoint="/api/complaints/" />
            </main>
            <Footer />
        </div>
    );
};

export default Home;
