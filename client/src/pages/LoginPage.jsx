import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const LoginPage = () => {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const { login, user, logout } = useAuth();
    const navigate = useNavigate();

    // Remove auto-redirect to give user control
    // React.useEffect(() => { ... }, [user]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        const result = await login(formData.username, formData.password);
        if (result.success) {
            navigate('/dashboard');
        } else {
            setError(result.error);
        }
    };

    if (user) {
        return (
            <div className="min-h-[80vh] flex items-center justify-center">
                <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md border border-gray-100 text-center">
                    <h2 className="text-2xl font-bold mb-4 text-gray-800">Welcome Back!</h2>
                    <p className="text-gray-600 mb-6">
                        You are already logged in as <span className="font-semibold">{user.username || 'User'}</span>.
                    </p>
                    <div className="space-y-3">
                        <button
                            onClick={() => navigate('/dashboard')}
                            className="w-full py-2 px-4 rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                        >
                            Go to Dashboard
                        </button>
                        <button
                            onClick={() => {
                                logout();
                                navigate('/login');
                            }}
                            className="w-full py-2 px-4 rounded-md border border-gray-300 shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                        >
                            Logout & Switch Account
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-[80vh] flex items-center justify-center">
            <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md border border-gray-100">
                <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Login to Jan Sevak</h2>

                {error && (
                    <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Username</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 border p-2"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 border p-2"
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                        Sign In
                    </button>
                </form>
                <div className="mt-4 text-center text-sm text-gray-600">
                    Don't have an account? <Link to="/register" className="text-blue-600 hover:underline">Register here</Link>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
