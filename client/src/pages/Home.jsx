import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';
import Navbar from '../components/Navbar';
import ComplaintList from '../components/ComplaintList';
import ComplaintForm from '../components/ComplaintForm';
import Footer from '../components/Footer';

const Home = () => {
    const [showForm, setShowForm] = useState(false);
    const [refreshKey, setRefreshKey] = useState(0);
    const { user } = useAuth();
    const navigate = useNavigate();
    const { t } = useTranslation();

    // Redirect to login if not authenticated
    React.useEffect(() => {
        if (!user) {
            navigate('/login');
        }
    }, [user, navigate]);

    if (!user) return null; // Don't render anything while redirecting

    const handleSuccess = () => {
        setShowForm(false);
        setRefreshKey(old => old + 1);
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            <Navbar showForm={showForm} setShowForm={setShowForm} />

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
                {/* Features Section */}{/* Hero Section (Only visible if no complaints or explicitly desired, but for now keeping it simple as per original design which was just the list) */}
                {/* Actually, the original Home component just rendered ComplaintList. 
            The "Landing Page" design I created earlier was for a public landing page.
            Since the user is redirected to login immediately if not auth, this "Home" is actually the "User Feed".
            
            However, I should probably create a separate "LandingPage" for unauthenticated users 
            instead of forcing login immediately, to show off the "Fix Your City" marketing content.
            
            For now, I will stick to the existing logic: Authenticated Home = Feed. 
            But I will add the translations to the "ComplaintForm" and "ComplaintList" components instead.
        */}

                {showForm && (
                    <ComplaintForm onSuccess={handleSuccess} />
                )}

                <div className="mb-6">
                    <h1 className="text-2xl font-bold text-gray-900">{t('dashboard.my_complaints')}</h1>
                    {/* Note: In the original code it was just the list. I'm adding a header to verify i18n */}
                </div>

                <ComplaintList key={refreshKey} />
            </main>
            <Footer />
        </div>
    );
};

export default Home;
