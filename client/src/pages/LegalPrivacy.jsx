import React from 'react';
import Navbar from '../components/Navbar';

const PrivacyPolicy = () => {
    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 md:p-12">
                    <h1 className="text-3xl font-heading font-bold text-gray-900 mb-6">Privacy Policy</h1>
                    <p className="text-gray-500 mb-8">Last Updated: December 2025</p>

                    <div className="prose prose-blue max-w-none text-gray-600 space-y-6">
                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">1. Introduction</h2>
                            <p>
                                Welcome to <strong>Jan Sevak</strong> ("we," "our," or "us"). We are committed to protecting your privacy.
                                This Privacy Policy explains how we collect, use, and share your personal information when you use our platform
                                to report civic issues.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">2. Information We Collect</h2>
                            <ul className="list-disc pl-5 space-y-2">
                                <li><strong>Account Information:</strong> When you register, we collect your username and email address.</li>
                                <li><strong>Report Data:</strong> We collect the photos, descriptions, and location data (GPS coordinates) of the civic issues you report.</li>
                                <li><strong>Usage Data:</strong> We may collect anonymous data about how you interact with our app to improve performance.</li>
                            </ul>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">3. How We Use Your Information</h2>
                            <p>We use your data solely for the purpose of civic improvement:</p>
                            <ul className="list-disc pl-5 space-y-2">
                                <li>To display civic issues on our public map.</li>
                                <li>To analyze and prioritize issues using AI.</li>
                                <li>To generate reports for municipal authorities (e.g., BMC).</li>
                                <li>To track your contribution points and leaderboard status.</li>
                            </ul>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">4. Public Visibility</h2>
                            <p>
                                <strong>Important:</strong> Any civic issue you report (including photos and location) will be publicly visible on our platform.
                                However, your identity (username) can be hidden if you choose the "Report Anonymously" option.
                                We will <strong>never</strong> publicly share your email address.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">5. Data Security</h2>
                            <p>
                                We implement reasonable security measures to protect your data. However, no method of transmission over the Internet is 100% secure.
                                We use standard encryption and secure database practices.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">6. Contact Us</h2>
                            <p>
                                If you have any questions about this policy, please contact us at: <a href="mailto:contact@jansevak.co.in" className="text-blue-600 hover:underline">contact@jansevak.co.in</a>
                            </p>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PrivacyPolicy;
