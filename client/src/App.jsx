import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import ComplaintList from './components/ComplaintList';
import ComplaintForm from './components/ComplaintForm';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import MapPage from './pages/MapPage';
import LeaderboardPage from './pages/LeaderboardPage';
import LegalPrivacy from './pages/LegalPrivacy';
import Terms from './pages/Terms';
import Footer from './components/Footer';

import Home from './pages/Home';

import { ComplaintProvider } from './context/ComplaintContext';
import ComplaintModal from './components/ComplaintModal';

function App() {
  return (
    <AuthProvider>
      <ComplaintProvider>
        <Router>
          <ComplaintModal />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={
              <div className="min-h-screen bg-gray-50 flex flex-col">
                <Navbar />
                <div className="flex-grow">
                  <DashboardPage />
                </div>
                <Footer />
              </div>
            } />
            <Route path="/map" element={
              <div className="h-screen bg-gray-50 flex flex-col">
                <Navbar />
                <div className="flex-grow relative">
                  <MapPage />
                </div>
                <Footer />
              </div>
            } />
            <Route path="/leaderboard" element={
              <div className="min-h-screen bg-gray-50 flex flex-col">
                <Navbar />
                <div className="flex-grow">
                  <LeaderboardPage />
                </div>
                <Footer />
              </div>
            } />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/privacy" element={<LegalPrivacy />} />
            <Route path="/terms" element={<Terms />} />
          </Routes>
        </Router>
      </ComplaintProvider>
    </AuthProvider>
  );
}

export default App;
