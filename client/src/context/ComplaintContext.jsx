import React, { createContext, useState, useContext } from 'react';

const ComplaintContext = createContext();

export const useComplaint = () => {
    return useContext(ComplaintContext);
};

export const ComplaintProvider = ({ children }) => {
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [complaintUpdateTrigger, setComplaintUpdateTrigger] = useState(0);

    const openForm = () => setIsFormOpen(true);
    const closeForm = () => setIsFormOpen(false);

    const triggerUpdate = () => {
        setComplaintUpdateTrigger(prev => prev + 1);
    };

    const value = {
        isFormOpen,
        openForm,
        closeForm,
        complaintUpdateTrigger,
        triggerUpdate
    };

    return (
        <ComplaintContext.Provider value={value}>
            {children}
        </ComplaintContext.Provider>
    );
};
