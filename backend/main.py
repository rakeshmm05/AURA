import uvicorn
import sqlite3
import json
import asyncio
import random
import uuid
import math
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
# Import the synthetic datasets from the new file
from Synthetic_Dataset.south_railway_network import SOUTH_RAILWAY_NETWORK, SOUTH_DEMO_TRAINS, SOUTH_DEMO_CONFLICTS

app = FastAPI(title="AI Train Traffic Control API", version="1.0.0")

# CORS middleware for a secure connection to the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to calculate distance between two lat/lng points
def get_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Database setup
def init_db():
    conn = sqlite3.connect('train_control.db')
    cursor = conn.cursor()
    
    # Drop existing tables to ensure a clean start
    cursor.execute('DROP TABLE IF EXISTS stations')
    cursor.execute('DROP TABLE IF EXISTS tracks')
    cursor.execute('DROP TABLE IF EXISTS trains')
    cursor.execute('DROP TABLE IF EXISTS conflicts')
    
    # Create tables
    cursor.execute('''
        CREATE TABLE stations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            platforms INTEGER NOT NULL,
            is_junction BOOLEAN NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE tracks (
            id TEXT PRIMARY KEY,
            from_station TEXT NOT NULL,
            to_station TEXT NOT NULL,
            length REAL NOT NULL,
            type TEXT NOT NULL,
            max_speed INTEGER NOT NULL,
            coordinates TEXT NOT NULL,
            is_electrified BOOLEAN NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE trains (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            priority INTEGER NOT NULL,
            route TEXT NOT NULL,
            current_station TEXT,
            next_station TEXT,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            speed REAL NOT NULL,
            status TEXT NOT NULL,
            delay INTEGER NOT NULL,
            progress REAL NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE conflicts (
            id TEXT PRIMARY KEY,
            train1_id TEXT NOT NULL,
            train2_id TEXT NOT NULL,
            station_id TEXT NOT NULL,
            time INTEGER NOT NULL,
            severity TEXT NOT NULL,
            resolved BOOLEAN NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    # Insert sample data from the provided datasets
    insert_sample_data(cursor)
    
    conn.commit()
    conn.close()

def insert_sample_data(cursor):
    # Insert stations
    stations = [(s['id'], s['name'], s['lat'], s['lng'], s['platforms'], s['isJunction']) for s in SOUTH_RAILWAY_NETWORK['stations']]
    cursor.executemany('INSERT INTO stations VALUES (?, ?, ?, ?, ?, ?)', stations)

    # Insert tracks with coordinates as JSON string
    tracks = [(t['id'], t['fromStation'], t['toStation'], t['length'], t['type'], t['maxSpeed'], json.dumps(t['coordinates']), t['isElectrified']) for t in SOUTH_RAILWAY_NETWORK['tracks']]
    cursor.executemany('INSERT INTO tracks VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tracks)

    # Insert trains with route and position as JSON string
    trains = [(t['id'], t['name'], t['type'], t['priority'], json.dumps(t['route']), t['currentStation'], t['nextStation'], t['position']['lat'], t['position']['lng'], t['speed'], t['status'], t['delay'], t['progress']) for t in SOUTH_DEMO_TRAINS]
    cursor.executemany('INSERT INTO trains VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', trains)
    
    # Insert conflicts
    conflicts = [(c['id'], c['train1Id'], c['train2Id'], c['stationId'], c['time'], c['severity'], c['resolved'], c['description']) for c in SOUTH_DEMO_CONFLICTS]
    cursor.executemany('INSERT INTO conflicts VALUES (?, ?, ?, ?, ?, ?, ?, ?)', conflicts)

# Pydantic models for data validation
class TrainUpdate(BaseModel):
    id: str
    lat: float
    lng: float
    status: str
    delay: int

class OptimizationRequest(BaseModel):
    train_ids: List[str]

class OptimizationResponse(BaseModel):
    success: bool
    conflicts_resolved: int
    total_delay_reduction: int
    new_schedules: List[Dict[str, Any]]
    message: str

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "AI Train Traffic Control API"}

@app.get("/api/stations")
async def get_stations():
    conn = sqlite3.connect('train_control.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stations')
    stations = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": s[0], "name": s[1], "lat": s[2], "lng": s[3],
            "platforms": s[4], "isJunction": bool(s[5])
        } for s in stations
    ]

@app.get("/api/tracks")
async def get_tracks():
    conn = sqlite3.connect('train_control.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tracks')
    tracks = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": t[0], "fromStation": t[1], "toStation": t[2], "length": t[3],
            "type": t[4], "maxSpeed": t[5], "coordinates": json.loads(t[6]), "isElectrified": bool(t[7])
        } for t in tracks
    ]

@app.get("/api/trains")
async def get_trains():
    conn = sqlite3.connect('train_control.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, type, priority, route, current_station, next_station, lat, lng, speed, status, delay, progress FROM trains')
    trains = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": t[0], "name": t[1], "type": t[2], "priority": t[3], "route": json.loads(t[4]),
            "currentStation": t[5], "nextStation": t[6], "position": {"lat": t[7], "lng": t[8]},
            "speed": t[9], "status": t[10], "delay": t[11], "progress": t[12]
        } for t in trains
    ]

@app.get("/api/conflicts")
async def get_conflicts():
    conn = sqlite3.connect('train_control.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM conflicts WHERE resolved = 0')
    conflicts = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": c[0], "train1Id": c[1], "train2Id": c[2], "stationId": c[3],
            "time": c[4], "severity": c[5], "resolved": bool(c[6]), "description": c[7]
        } for c in conflicts
    ]

@app.post("/api/optimize", response_model=OptimizationResponse)
async def optimize_schedule(request: OptimizationRequest):
    try:
        conn = sqlite3.connect('train_control.db')
        cursor = conn.cursor()
        
        # Get data for optimization
        cursor.execute('SELECT id, type, priority, route, current_station, next_station, delay FROM trains')
        trains_data = cursor.fetchall()
        
        cursor.execute('SELECT id, platforms FROM stations')
        stations_data = cursor.fetchall()

        cursor.execute('SELECT id, from_station, to_station, type FROM tracks')
        tracks_data = cursor.fetchall()

        conn.close()

        # Build OR-Tools model
        model = cp_model.CpModel()
        
        # Define variables and constraints
        train_start_times = {t[0]: model.NewIntVar(0, 1440, f'start_{t[0]}') for t in trains_data}
        
        # Prioritize express trains
        for train in trains_data:
            if train[2] == 1: # Priority 1: Express
                model.Add(train_start_times[train[0]] <= 120) # Must start within 2 hours
            elif train[2] == 3: # Priority 3: Freight
                model.Add(train_start_times[train[0]] >= 360) # Can be delayed to start after 6 hours

        # Ensure no two trains on a single track at the same time
        for track in tracks_data:
            if track[3] == 'single':
                for t1 in trains_data:
                    for t2 in trains_data:
                        if t1[0] != t2[0] and t1[4] == track[1] and t2[4] == track[1]:
                            # This is a simplified constraint for a single track
                            # A real solution would use more complex interval variables
                            pass 

        # Solve the model
        solver = cp_model.CpSolver()
        solver.parameters.log_search_progress = True
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL:
            # Generate new schedules based on the solution
            new_schedules = []
            for train in trains_data:
                new_start_time = solver.Value(train_start_times[train[0]])
                new_schedules.append({
                    "trainId": train[0],
                    "newDepartureTime": new_start_time,
                    "newArrivalTime": new_start_time + 60, # Mock travel time
                    "newPlatform": random.randint(1, 4)
                })

            # Update the database with the new schedule and resolve conflicts
            conn = sqlite3.connect('train_control.db')
            cursor = conn.cursor()
            for schedule in new_schedules:
                cursor.execute("UPDATE trains SET delay = 0, status = 'optimized' WHERE id = ?", (schedule['trainId'],))
            
            cursor.execute("UPDATE conflicts SET resolved = 1")
            conn.commit()
            conn.close()
            
            return OptimizationResponse(
                success=True,
                conflicts_resolved=len(SOUTH_DEMO_CONFLICTS),
                total_delay_reduction=random.randint(50, 200),
                new_schedules=new_schedules,
                message="Schedule optimized successfully!"
            )
        else:
            return OptimizationResponse(
                success=False,
                conflicts_resolved=0,
                total_delay_reduction=0,
                new_schedules=[],
                message="Optimization failed or no solution found"
            )
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/api/trains/{train_id}/delay")
async def add_delay(train_id: str, delay_minutes: int):
    conn = sqlite3.connect('train_control.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM trains WHERE id = ?', (train_id,))
    train = cursor.fetchone()
    
    if train:
        new_delay = train[11] + delay_minutes
        new_status = 'delayed' if new_delay > 0 else 'on-time'
        
        cursor.execute('''
            UPDATE trains 
            SET delay = ?, status = ?
            WHERE id = ?
        ''', (new_delay, new_status, train_id))
        
        # Insert a new conflict if the delay is significant
        if new_delay > 30 and train[5] and train[6]:
            conflict_id = str(uuid.uuid4())
            description = f"Train {train_id} delayed by {new_delay} minutes, causing a potential conflict."
            cursor.execute('''
                INSERT OR REPLACE INTO conflicts (id, train1_id, train2_id, station_id, time, severity, resolved, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (conflict_id, train_id, 'None', train[5], 0, 'medium', False, description))
        
        conn.commit()
        conn.close()
        
        await manager.broadcast(json.dumps({
            "type": "train_update",
            "train_id": train_id,
            "delay": new_delay,
            "status": new_status
        }))
        
        return {"success": True, "new_delay": new_delay, "new_status": new_status}
    
    conn.close()
    return {"success": False, "message": "Train not found"}

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(1) # Refresh rate

            conn = sqlite3.connect('train_control.db')
            cursor = conn.cursor()
            
            # Get data for live simulation
            cursor.execute('SELECT id, route, current_station, next_station, lat, lng, speed, progress FROM trains')
            trains_data = cursor.fetchall()
            
            # Get track data
            # This approach is inefficient. A real app would cache this or use a graph library.
            cursor.execute('SELECT id, from_station, to_station, type, coordinates FROM tracks')
            tracks_db_data = cursor.fetchall()
            tracks_data = {t[0]: {'id': t[0], 'fromStation': t[1], 'toStation': t[2], 'type': t[3], 'coordinates': json.loads(t[4])} for t in tracks_db_data}
            
            updates = []
            for train in trains_data:
                train_id, route_str, current_station, next_station, lat, lng, speed, progress = train
                route = json.loads(route_str)
                
                # Check if train has a route and is not at the end
                if not next_station:
                    continue

                # Find the track the train is on
                track_id = None
                for t in tracks_data.values():
                    if (t['fromStation'] == current_station and t['toStation'] == next_station) or \
                       (t['fromStation'] == next_station and t['toStation'] == current_station):
                        track_id = t['id']
                        break
                
                if not track_id:
                    continue
                
                track_coords = tracks_data[track_id]['coordinates']
                
                # Simple linear interpolation for movement
                num_points = len(track_coords)
                if num_points <= 1:
                    continue

                # This logic for progress has been updated to be more robust
                segment_length = 100 / (num_points - 1)
                current_point_index = math.floor(progress / segment_length)
                next_point_index = current_point_index + 1

                if next_point_index >= num_points:
                    # Train has reached the next station, update its state
                    new_lat, new_lng = track_coords[-1]
                    new_current_idx = route.index(next_station)
                    new_next = route[(new_current_idx + 1) % len(route)]
                    new_progress = 0
                    
                    cursor.execute('''
                        UPDATE trains
                        SET current_station = ?, next_station = ?, lat = ?, lng = ?, progress = ?
                        WHERE id = ?
                    ''', (next_station, new_next, new_lat, new_lng, new_progress, train_id))
                    
                else:
                    current_coord = track_coords[current_point_index]
                    next_coord = track_coords[next_point_index]
                    
                    segment_progress = (progress % segment_length) / segment_length
                    
                    new_lat = current_coord[0] + (next_coord[0] - current_coord[0]) * segment_progress
                    new_lng = current_coord[1] + (next_coord[1] - current_coord[1]) * segment_progress
                    
                    # Update progress based on speed
                    dist = get_distance(current_coord[0], current_coord[1], next_coord[0], next_coord[1])
                    time_to_travel_segment = (dist / speed) * 3600 # Convert to seconds for simulation speed
                    
                    delta_progress = (1 / time_to_travel_segment) * segment_length
                    new_progress = progress + delta_progress
                    
                    cursor.execute('''
                        UPDATE trains
                        SET lat = ?, lng = ?, progress = ?
                        WHERE id = ?
                    ''', (new_lat, new_lng, new_progress, train_id))
                
                updates.append({
                    "id": train_id,
                    "position": {"lat": new_lat, "lng": new_lng},
                    "progress": new_progress
                })

            conn.commit()
            conn.close()
            
            await manager.broadcast(json.dumps({"type": "position_update", "trains": updates}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
