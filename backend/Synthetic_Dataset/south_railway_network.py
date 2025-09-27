# This file contains the complete synthetic dataset for the South Indian railway network.
# It is stored separately to keep the main application logic clean and modular.

SOUTH_RAILWAY_NETWORK = {
  "stations": [
    {
      "id": "SBC", "name": "KSR Bengaluru", "lat": 12.9774, "lng": 77.5701,
      "platforms": 10, "isJunction": True, "type": "junction", "capacity": 350
    },
    {
      "id": "MAS", "name": "Chennai Central", "lat": 13.0827, "lng": 80.2707,
      "platforms": 17, "isJunction": True, "type": "junction", "capacity": 400
    },
    {
      "id": "SC", "name": "Secunderabad Junction", "lat": 17.4399, "lng": 78.4746,
      "platforms": 10, "isJunction": True, "type": "junction", "capacity": 300
    },
    {
      "id": "JTJ", "name": "Jolarpettai Junction", "lat": 12.5695, "lng": 78.5772,
      "platforms": 5, "isJunction": True, "type": "junction", "capacity": 150
    },
    {
      "id": "GTL", "name": "Guntakal Junction", "lat": 15.1764, "lng": 77.3688,
      "platforms": 7, "isJunction": True, "type": "junction", "capacity": 180
    },
    {
      "id": "CBE", "name": "Coimbatore Junction", "lat": 11.0055, "lng": 76.9662,
      "platforms": 6, "isJunction": True, "type": "junction", "capacity": 160
    },
    {
      "id": "ERS", "name": "Ernakulam Junction", "lat": 9.9678, "lng": 76.2934,
      "platforms": 6, "isJunction": True, "type": "junction", "capacity": 220
    }
  ],
  "tracks": [
    { "id": "T101", "fromStation": "SBC", "toStation": "MAS", "length": 362, "type": "double", "maxSpeed": 130, "coordinates": [[12.9774, 77.5701], [12.85, 77.95], [12.7, 78.4], [12.65, 78.7], [12.8, 79.2], [12.9, 79.8], [13.0827, 80.2707]], "isElectrified": True },
    { "id": "T102", "fromStation": "SBC", "toStation": "SC", "length": 575, "type": "double", "maxSpeed": 120, "coordinates": [[12.9774, 77.5701], [14.0, 77.5], [15.0, 77.4], [16.0, 77.8], [17.0, 78.2], [17.4399, 78.4746]], "isElectrified": True },
    { "id": "T103", "fromStation": "MAS", "toStation": "SC", "length": 660, "type": "double", "maxSpeed": 110, "coordinates": [[13.0827, 80.2707], [13.5, 79.8], [14.0, 79.2], [15.0, 78.5], [16.0, 78.3], [17.0, 78.4], [17.4399, 78.4746]], "isElectrified": True },
    { "id": "T104", "fromStation": "SBC", "toStation": "JTJ", "length": 145, "type": "double", "maxSpeed": 120, "coordinates": [[12.9774, 77.5701], [12.8, 77.8], [12.6, 78.2], [12.5695, 78.5772]], "isElectrified": True },
    { "id": "T105", "fromStation": "JTJ", "toStation": "MAS", "length": 130, "type": "double", "maxSpeed": 110, "coordinates": [[12.5695, 78.5772], [12.8, 79.2], [13.0, 79.8], [13.0827, 80.2707]], "isElectrified": True },
    { "id": "T106", "fromStation": "CBE", "toStation": "ERS", "length": 190, "type": "double", "maxSpeed": 100, "coordinates": [[11.0055, 76.9662], [10.8, 76.8], [10.4, 76.5], [9.9678, 76.2934]], "isElectrified": True },
    { "id": "T107", "fromStation": "SBC", "toStation": "CBE", "length": 378, "type": "double", "maxSpeed": 100, "coordinates": [[12.9774, 77.5701], [12.5, 77.2], [11.8, 77.0], [11.5, 76.9], [11.0055, 76.9662]], "isElectrified": True },
    { "id": "T108", "fromStation": "SC", "toStation": "GTL", "length": 300, "type": "double", "maxSpeed": 100, "coordinates": [[17.4399, 78.4746], [16.5, 78.0], [15.8, 77.5], [15.1764, 77.3688]], "isElectrified": True },
    { "id": "T109", "fromStation": "GTL", "toStation": "SBC", "length": 290, "type": "single", "maxSpeed": 90, "coordinates": [[15.1764, 77.3688], [14.5, 77.4], [13.8, 77.5], [12.9774, 77.5701]], "isElectrified": False }
  ]
}

SOUTH_DEMO_TRAINS = [
  { "id": "T1", "name": "Vande Bharat Express", "type": "express", "priority": 1, "route": ["SBC", "JTJ", "MAS"], "currentStation": "SBC", "nextStation": "JTJ", "position": {"lat": 12.9774, "lng": 77.5701}, "speed": 130, "status": "at-station", "delay": 0, "icon": "🚄", "progress": 0 },
  { "id": "T2", "name": "Rajdhani Express", "type": "express", "priority": 1, "route": ["SC", "GTL", "SBC"], "currentStation": "SC", "nextStation": "GTL", "position": {"lat": 17.4399, "lng": 78.4746}, "speed": 120, "status": "on-time", "delay": 0, "icon": "🚄", "progress": 10 },
  { "id": "T3", "name": "Intercity Express", "type": "passenger", "priority": 2, "route": ["MAS", "JTJ", "SBC", "CBE", "ERS"], "currentStation": "MAS", "nextStation": "JTJ", "position": {"lat": 13.0827, "lng": 80.2707}, "speed": 95, "status": "on-time", "delay": 0, "icon": "🚃", "progress": 5 },
  { "id": "T4", "name": "Freight Carrier Alpha", "type": "freight", "priority": 3, "route": ["SC", "GTL", "SBC", "CBE", "ERS"], "currentStation": "SC", "nextStation": "GTL", "position": {"lat": 17.4399, "lng": 78.4746}, "speed": 60, "status": "delayed", "delay": 45, "icon": "🚂", "progress": 20 },
  { "id": "T5", "name": "Local Passenger", "type": "passenger", "priority": 2, "route": ["ERS", "CBE", "SBC"], "currentStation": "ERS", "nextStation": "CBE", "position": {"lat": 9.9678, "lng": 76.2934}, "speed": 80, "status": "on-time", "delay": 0, "icon": "🚃", "progress": 0 }
]

SOUTH_DEMO_CONFLICTS = [
  { "id": "C1", "train1Id": "T1", "train2Id": "T3", "stationId": "JTJ", "time": 720, "severity": "high", "resolved": False, "description": "High-speed Vande Bharat and Intercity Express scheduled to arrive at the same platform at Jolarpettai Junction." },
  { "id": "C2", "train1Id": "T4", "train2Id": "T2", "stationId": "GTL", "time": 960, "severity": "medium", "resolved": False, "description": "Delayed freight train blocking a higher-priority express train at Guntakal Junction." }
]
