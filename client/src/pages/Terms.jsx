import React from 'react';
import Navbar from '../components/Navbar';

const Terms = () => {
    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 md:p-12">
                    <h1 className="text-3xl font-heading font-bold text-gray-900 mb-6">Terms and Conditions</h1>
                    <p className="text-gray-500 mb-8">Last Updated: December 2025</p>

                    <div className="prose prose-blue max-w-none text-gray-600 space-y-6">
                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">1. Acceptance of Terms</h2>
                            <p>
                                By accessing or using <strong>Jan Sevak</strong>, you agree to be bound by these Terms and Conditions.
                                If you do not agree, please do not use our platform.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">2. Description of Service</h2>
                            <p>
                                Jan Sevak is a community-driven platform for reporting and tracking civic issues.
                                <strong>Disclaimer:</strong> We are an independent initiative and are <strong>not</strong> officially affiliated with the Brihanmumbai Municipal Corporation (BMC) or any other government body.
                                We act as an intermediary to highlight issues using data.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">3. User Responsibilities</h2>
                            <p>You agree to:</p>
                            <ul className="list-disc pl-5 space-y-2">
                                <li>Provide accurate and truthful information when reporting issues.</li>
                                <li>Not upload content that is offensive, abusive, or irrelevant.</li>
                                <li>Not use the platform for any illegal or unauthorized purpose.</li>
                                <li>Respect the privacy of others in your photos (avoid capturing faces or private property clearly).</li>
                            </ul>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">4. Content Moderation</h2>
                            <p>
                                We use AI and manual moderation to review reports. We reserve the right to remove any content that violates these terms
                                or is deemed inappropriate, without prior notice.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">5. Limitation of Liability</h2>
                            <p>
                                Jan Sevak is provided "as is." We do not guarantee that reporting an issue on our platform will result in its resolution by the authorities.
                                We are not liable for any damages arising from your use of the platform.
                            </p>
                        </section>

                        <section>
                            <h2 className="text-xl font-bold text-gray-900 mb-3">6. Changes to Terms</h2>
                            <p>
                                We may update these terms from time to time. Your continued use of the platform constitutes acceptance of the new terms.
                            </p>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Terms;
