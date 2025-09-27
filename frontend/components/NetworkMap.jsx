import React from 'react';
import { MapContainer, TileLayer, Marker, Polyline, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { SOUTH_RAILWAY_NETWORK, SOUTH_DEMO_TRAINS } from '../../Synthetic_Dataset/south_railway_network.py';

// Fix for default Leaflet icons not appearing in some environments
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

export default function NetworkMap() {
  const center = [14.0, 78.0]; // Center of the map, roughly in South India
  const tracks = SOUTH_RAILWAY_NETWORK.tracks;
  const stations = SOUTH_RAILWAY_NETWORK.stations;
  const trains = SOUTH_DEMO_TRAINS;

  return (
    <div className="h-full w-full rounded-lg shadow-lg overflow-hidden z-0">
      <MapContainer center={center} zoom={6} className="h-full w-full z-0">
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />

        {/* Render Tracks */}
        {tracks.map(track => (
          <Polyline
            key={track.id}
            positions={track.coordinates}
            color={track.type === 'single' ? 'orange' : 'blue'}
            weight={3}
            opacity={0.8}
          >
            <Popup>
              <div>
                <h4 className="font-bold">{track.id}</h4>
                <p>From: {track.fromStation} to: {track.toStation}</p>
                <p>Type: {track.type}</p>
                <p>Length: {track.length} km</p>
              </div>
            </Popup>
          </Polyline>
        ))}

        {/* Render Stations */}
        {stations.map(station => (
          <Marker key={station.id} position={[station.lat, station.lng]}>
            <Popup>
              <div>
                <h4 className="font-bold">{station.name} ({station.id})</h4>
                <p>Platforms: {station.platforms}</p>
                <p>Type: {station.type}</p>
              </div>
            </Popup>
          </Marker>
        ))}
        
        {/* Render Trains */}
        {trains.map(train => (
          <Marker
            key={train.id}
            position={[train.position.lat, train.position.lng]}
            icon={L.divIcon({
              className: 'custom-train-icon',
              html: `<div style="font-size: 24px;">${train.icon}</div>`,
              iconSize: [24, 24],
              iconAnchor: [12, 12],
            })}
          >
            <Popup>
              <div>
                <h4 className="font-bold">{train.name}</h4>
                <p>ID: {train.id}</p>
                <p>Status: {train.status}</p>
                <p>Current Station: {train.currentStation}</p>
                <p>Next Station: {train.nextStation}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
