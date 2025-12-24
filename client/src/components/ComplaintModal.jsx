import React, { useEffect } from 'react';
import { useComplaint } from '../context/ComplaintContext';
import ComplaintForm from './ComplaintForm';
import { useTranslation } from 'react-i18next';
import { useLocation } from 'react-router-dom';

const ComplaintModal = () => {
    const { isFormOpen, closeForm, triggerUpdate } = useComplaint();
    const { t } = useTranslation();
    const location = useLocation();

    // Close modal when route changes
    useEffect(() => {
        if (isFormOpen) {
            closeForm();
        }
    }, [location.pathname]);

    if (!isFormOpen) return null;

    const handleSuccess = () => {
        triggerUpdate();
        closeForm();
    };

    return (
        <div className="fixed inset-0 z-[90] overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            {/* Backdrop */}
            <div
                className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
                aria-hidden="true"
                onClick={closeForm}
            ></div>

            <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                {/* Centering trick */}
                <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

                {/* Modal Panel */}
                <div className="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">

                    {/* Close Button */}
                    <div className="absolute top-0 right-0 pt-4 pr-4 z-10">
                        <button
                            type="button"
                            className="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                            onClick={closeForm}
                        >
                            <span className="sr-only">{t('common.close')}</span>
                            <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    {/* Content */}
                    <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <ComplaintForm onSuccess={handleSuccess} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ComplaintModal;
