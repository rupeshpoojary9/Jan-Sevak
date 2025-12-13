import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Check if user is logged in on mount
    useEffect(() => {
        // Configure Axios to include CSRF token from cookie
        const getCookie = (name) => {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        };

        const csrftoken = getCookie('csrftoken');
        if (csrftoken) {
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken;
        }

        checkUserStatus();
    }, []);

    const checkUserStatus = async () => {
        try {
            // dj-rest-auth endpoint to get current user details
            const response = await axios.get('/auth/user/');
            let userData = response.data;

            // Set axios default header if user is logged in
            if (userData && userData.key) {
                axios.defaults.headers.common['Authorization'] = `Token ${userData.key}`;
            } else if (userData && userData.access_token) {
                axios.defaults.headers.common['Authorization'] = `Bearer ${userData.access_token}`;
            }

            // Fetch Gamification Profile (Points)
            try {
                const profileRes = await axios.get('/api/leaderboard/my_profile/');
                userData = { ...userData, ...profileRes.data };
            } catch (err) {
                console.warn("Failed to fetch user profile", err);
            }

            setUser(userData);

            // Ensure header is set if session/cookie auth is working
            // Note: dj-rest-auth with JWT cookies might handle this automatically for browser,
            // but for explicit token usage we might need to set it.
            // However, since we are using cookies, the browser sends them automatically.
            // The issue might be CSRF or that we are NOT using the token from the response if it's cookie only.

            // Wait, if we are using JWT cookies, we don't need to set the header manually IF the backend looks for cookies.
            // But our backend settings have:
            // REST_FRAMEWORK = { ... 'DEFAULT_AUTHENTICATION_CLASSES': ['dj_rest_auth.jwt_auth.JWTCookieAuthentication'] ... }
            // So cookies should work.

            // Let's check if the previous complaints were actually anonymous.
        } catch (error) {
            // Not logged in
            setUser(null);
            delete axios.defaults.headers.common['Authorization']; // Clear header if not logged in
        } finally {
            setLoading(false);
        }
    };

    const login = async (username, password) => {
        try {
            await axios.post('/auth/login/', { username, password });
            await checkUserStatus(); // Refresh user data
            return { success: true };
        } catch (error) {
            return { success: false, error: error.response?.data?.non_field_errors?.[0] || 'Login failed' };
        }
    };

    const register = async (username, email, password) => {
        try {
            await axios.post('/auth/registration/', {
                username,
                email,
                password1: password,
                password2: password
            });
            // Explicitly login after registration to ensure cookie is set
            return await login(username, password);
        } catch (error) {
            return { success: false, error: error.response?.data };
        }
    };

    const logout = async () => {
        try {
            await axios.post('/auth/logout/');
            setUser(null);
        } catch (error) {
            console.error("Logout failed", error);
        }
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
