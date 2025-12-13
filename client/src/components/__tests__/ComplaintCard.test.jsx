import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ComplaintCard from '../ComplaintCard';
import { AuthContext } from '../../context/AuthContext';

// Mock Auth Context
const mockUser = { pk: 1, username: 'tester' };
const mockAuthContext = {
    user: mockUser,
    loading: false,
};

// Mock Complaint Data
const mockComplaint = {
    id: 1,
    title: 'Test Pothole',
    description: 'Big hole',
    ward_name: 'A Ward',
    status: 'NEW',
    urgency_score: 8,
    image: 'http://test.com/image.jpg',
    reporter: 1, // Matches mockUser
    created_at: '2023-01-01T00:00:00Z',
    verification_count: 5,
    is_verified: false
};

const renderWithAuth = (ui, authValue = mockAuthContext) => {
    return render(
        <AuthContext.Provider value={authValue}>
            {ui}
        </AuthContext.Provider>
    );
};

describe('ComplaintCard', () => {
    it('renders complaint details correctly', () => {
        renderWithAuth(<ComplaintCard complaint={mockComplaint} />);

        expect(screen.getByText('Test Pothole')).toBeInTheDocument();
        expect(screen.getByText('A Ward')).toBeInTheDocument();
        expect(screen.getByText('Big hole')).toBeInTheDocument();
        expect(screen.getByText(/Urgency\s*8\/10/)).toBeInTheDocument();
    });

    it('shows Delete button for owner when status is NEW', () => {
        const onDelete = vi.fn();
        renderWithAuth(<ComplaintCard complaint={mockComplaint} onDelete={onDelete} />);

        const deleteBtn = screen.getByTitle('Delete');
        expect(deleteBtn).toBeInTheDocument();
    });

    it('does NOT show Delete button for non-owner', () => {
        const otherUserAuth = { ...mockAuthContext, user: { pk: 2 } };
        renderWithAuth(<ComplaintCard complaint={mockComplaint} />, otherUserAuth);

        const deleteBtn = screen.queryByTitle('Delete');
        expect(deleteBtn).not.toBeInTheDocument();
    });

    it('does NOT show Delete button if status is not NEW', () => {
        const processedComplaint = { ...mockComplaint, status: 'VERIFIED' };
        renderWithAuth(<ComplaintCard complaint={processedComplaint} />);

        const deleteBtn = screen.queryByTitle('Delete');
        expect(deleteBtn).not.toBeInTheDocument();
    });
});
