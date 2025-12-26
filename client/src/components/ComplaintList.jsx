import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';
import ComplaintCard from './ComplaintCard';

const ComplaintList = ({ endpoint }) => {
    const [complaints, setComplaints] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchParams, setSearchParams] = useSearchParams();
    const [totalPages, setTotalPages] = useState(1);

    const [categoryFilter, setCategoryFilter] = useState('');
    const [urgencyFilter, setUrgencyFilter] = useState('');

    // Get params from URL
    const page = parseInt(searchParams.get('page') || '1');
    const searchQuery = searchParams.get('search') || '';
    const [debouncedSearch, setDebouncedSearch] = useState(searchQuery);

    // Debounce search input
    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedSearch(searchQuery);
        }, 500);
        return () => clearTimeout(timer);
    }, [searchQuery]);

    const fetchComplaints = async () => {
        setLoading(true);
        try {
            // Build URL with params
            let url = endpoint ? `${endpoint}?page=${page}` : `/api/complaints/?page=${page}`;
            if (debouncedSearch) {
                url += `&search=${debouncedSearch}`;
            }
            if (categoryFilter) {
                url += `&category=${categoryFilter}`;
            }
            if (urgencyFilter) {
                // Parse range "min-max" or single value "10"
                if (urgencyFilter.includes('-')) {
                    const [min, max] = urgencyFilter.split('-');
                    url += `&urgency_min=${min}&urgency_max=${max}`;
                } else {
                    url += `&urgency_min=${urgencyFilter}&urgency_max=${urgencyFilter}`;
                }
            }

            console.log("DEBUG: Fetching complaints from", url);
            const res = await axios.get(url);
            console.log("DEBUG: Complaints fetched:", res.data.results.length);
            setComplaints(res.data.results);

            // Calculate total pages (assuming default page size of 10 if not provided)
            const pageSize = 10;
            setTotalPages(Math.ceil(res.data.count / pageSize));

        } catch (err) {
            console.error("Failed to fetch complaints", err);
        } finally {
            setLoading(false);
        }
    };

    // Fetch when page, search, or filters change
    useEffect(() => {
        fetchComplaints();
        // Scroll to top on page change
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, [page, debouncedSearch, categoryFilter, urgencyFilter]);

    const handleSearchChange = (e) => {
        const text = e.target.value;
        // Update URL params
        if (text) {
            setSearchParams({ search: text, page: 1 });
        } else {
            setSearchParams({ page: 1 });
        }
    };

    const handlePageChange = (newPage) => {
        if (newPage >= 1 && newPage <= totalPages) {
            const params = { page: newPage };
            if (debouncedSearch) params.search = debouncedSearch;
            setSearchParams(params);
        }
    };

    return (
        <div className="space-y-6">
            {/* Search and Filters */}
            <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-8">
                {/* Search Bar */}
                <div className="relative w-full md:w-1/2">
                    <input
                        type="text"
                        placeholder="Search complaints..."
                        value={searchQuery}
                        onChange={handleSearchChange}
                        className="input-field pl-12"
                    />
                    <div className="absolute left-4 top-3.5 text-gray-400">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>
                </div>

                {/* Filters */}
                <div className="flex gap-2 w-full md:w-auto">
                    <select
                        value={categoryFilter}
                        onChange={(e) => { setCategoryFilter(e.target.value); setSearchParams({ page: 1 }); }}
                        className="input-field w-full md:w-40"
                    >
                        <option value="">All Categories</option>
                        <option value="POTHOLE">Pothole</option>
                        <option value="GARBAGE">Garbage</option>
                        <option value="DRAINAGE">Drainage</option>
                        <option value="LIGHTING">Street Lights</option>
                        <option value="WATER">Water Supply</option>
                        <option value="SANITATION">Sanitation</option>
                        <option value="TRAFFIC">Traffic</option>
                        <option value="PARKS">Parks</option>
                        <option value="OTHERS">Others</option>
                    </select>

                    <select
                        value={urgencyFilter}
                        onChange={(e) => { setUrgencyFilter(e.target.value); setSearchParams({ page: 1 }); }}
                        className="input-field w-full md:w-40"
                    >
                        <option value="">All Urgency</option>
                        <option value="10">Critical (10)</option>
                        <option value="8-10">High (8-10)</option>
                        <option value="4-7">Medium (4-7)</option>
                        <option value="1-3">Low (1-3)</option>
                    </select>
                </div>
            </div>

            {loading && (
                <div className="flex justify-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>
            )}

            {!loading && complaints.length === 0 && (
                <div className="text-center py-10 text-gray-500 bg-white rounded-xl border border-gray-100 shadow-sm">
                    <p className="text-lg font-medium">No complaints found</p>
                    <p className="text-sm">Try adjusting your filters</p>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {complaints.map(complaint => (
                    <ComplaintCard
                        key={complaint.id}
                        complaint={complaint}
                        onDelete={fetchComplaints}
                    />
                ))}
            </div>

            {/* Numbered Pagination Controls */}
            {!loading && totalPages > 1 && (
                <div className="flex justify-center items-center space-x-2 mt-12">
                    <button
                        onClick={() => handlePageChange(page - 1)}
                        disabled={page === 1}
                        className="p-2 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                    </button>

                    {/* Generate Page Numbers */}
                    {[...Array(totalPages)].map((_, i) => {
                        const pageNum = i + 1;
                        // Show first, last, current, and neighbors
                        if (
                            pageNum === 1 ||
                            pageNum === totalPages ||
                            (pageNum >= page - 1 && pageNum <= page + 1)
                        ) {
                            return (
                                <button
                                    key={pageNum}
                                    onClick={() => handlePageChange(pageNum)}
                                    className={`w-10 h-10 rounded-lg font-medium transition-all ${page === pageNum
                                        ? 'bg-blue-600 text-white shadow-md scale-105'
                                        : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50 hover:border-blue-300'
                                        }`}
                                >
                                    {pageNum}
                                </button>
                            );
                        } else if (
                            pageNum === page - 2 ||
                            pageNum === page + 2
                        ) {
                            return <span key={pageNum} className="text-gray-400">...</span>;
                        }
                        return null;
                    })}

                    <button
                        onClick={() => handlePageChange(page + 1)}
                        disabled={page === totalPages}
                        className="p-2 rounded-lg border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                        </svg>
                    </button>
                </div>
            )}
        </div>
    );
};

export default ComplaintList;
