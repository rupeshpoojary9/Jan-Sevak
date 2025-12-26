import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useComplaint } from '../context/ComplaintContext';

// Fix for default marker icon missing in Leaflet + Webpack/Vite
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapPage = () => {
    const [geoData, setGeoData] = useState(null);
    const [loading, setLoading] = useState(true);
    const { complaintUpdateTrigger } = useComplaint();

    // Center on Mumbai (Dadar)
    const position = [19.0178, 72.8478];

    useEffect(() => {
        const fetchGeoJSON = async () => {
            try {
                const res = await axios.get('/api/complaints/geojson/');
                setGeoData(res.data);
            } catch (err) {
                console.error("Failed to fetch map data", err);
            } finally {
                setLoading(false);
            }
        };
        fetchGeoJSON();
    }, [complaintUpdateTrigger]);

    if (loading) return <div className="text-center py-20">Loading Map...</div>;

    // Mumbai Bounds
    const mumbaiBounds = [
        [18.89, 72.75], // Southwest coordinates
        [19.30, 73.00]  // Northeast coordinates
    ];

    // Helper to create colored pin icon
    const createCustomIcon = (color) => {
        const svg = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${color}" width="36" height="36" stroke="white" stroke-width="1.5">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
            </svg>
        `;
        return L.divIcon({
            className: 'custom-pin-icon',
            html: svg,
            iconSize: [36, 36],
            iconAnchor: [18, 36], // Bottom center
            popupAnchor: [0, -36]
        });
    };

    return (
        <div className="h-[calc(100vh-64px)] w-full">
            <MapContainer
                center={position}
                zoom={12}
                scrollWheelZoom={true}
                style={{ height: '100%', width: '100%' }}
                maxBounds={mumbaiBounds}
                minZoom={11}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {geoData && geoData.features.map((feature) => {
                    const [lng, lat] = feature.geometry.coordinates;
                    const { title, category, status, urgency_score, ward_name } = feature.properties;

                    // Determine Color based on Urgency
                    let color = '#10B981'; // Green (Tailwind emerald-500)
                    if (urgency_score >= 8) color = '#EF4444'; // Red (Tailwind red-500)
                    else if (urgency_score >= 4) color = '#F59E0B'; // Orange (Tailwind amber-500)

                    return (
                        <Marker
                            key={feature.properties.id}
                            position={[lat, lng]}
                        >
                            <Popup>
                                <div className="p-1">
                                    <h3 className="font-bold text-sm">{title}</h3>
                                    <p className="text-xs text-gray-600">{category} • {ward_name}</p>
                                    <div className="mt-1 flex items-center gap-2">
                                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${status === 'RESOLVED' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                                            }`}>
                                            {status}
                                        </span>
                                        {urgency_score > 0 && (
                                            <span className={`text-xs font-bold ${urgency_score >= 8 ? 'text-red-600' : 'text-orange-600'}`}>
                                                Urgency: {urgency_score}/10
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </Popup>
                        </Marker>
                    );
                })}
            </MapContainer>
        </div>
    );
};

export default MapPage;
