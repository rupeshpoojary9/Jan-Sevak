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
    const { t } = useTranslation();
    const { complaintUpdateTrigger } = useComplaint();
    const [refreshKey, setRefreshKey] = useState(0);

    // Update refresh key when global trigger changes
    useEffect(() => {
        setRefreshKey(prev => prev + 1);
    }, [complaintUpdateTrigger]);

    // Redirect to Dashboard if logged in
    useEffect(() => {
        if (user) {
            navigate('/dashboard');
        }
    }, [user, navigate]);

    // Always show Landing Page at root (for guests)
    // Logged in users will be redirected by useEffect
    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            {/* Navbar hidden for guests on Landing Page */}
            {user && <Navbar />}
            <main className="flex-grow">
                <LandingPage />
            </main>
            <Footer />
        </div>
    );
};

export default Home;
