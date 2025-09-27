    import React from 'react';
    import NetworkMap from './NetworkMap';

    export default function Dashboard() {
      return (
        <div className="flex h-screen bg-gray-900 text-white">
          {/* Sidebar */}
          <div className="w-64 bg-gray-800 p-4">
            <h1 className="text-2xl font-bold">AURA</h1>
            <nav className="mt-8">
              <ul>
                <li className="mb-4">Dashboard</li>
                <li className="mb-4">Train Map</li>
                <li className="mb-4">Schedule</li>
                <li className="mb-4">AI Decisions</li>
                <li className="mb-4">Alerts</li>
                <li className="mb-4">Reports</li>
                <li className="mb-4">Settings</li>
              </ul>
            </nav>
          </div>

          {/* Main Content Area */}
          <div className="flex-1 p-8">
            <header className="flex justify-between items-center mb-8">
              <h2 className="text-3xl font-bold">AI Dashboard</h2>
              <button className="bg-blue-600 px-4 py-2 rounded-lg font-semibold">
                Run AI Optimization
              </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                <h3 className="text-sm text-gray-400">Trains Running</h3>
                <p className="text-4xl font-bold mt-2">24</p>
              </div>
              <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                <h3 className="text-sm text-gray-400">Avg Delay (min)</h3>
                <p className="text-4xl font-bold mt-2 text-yellow-400">12</p>
              </div>
              <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                <h3 className="text-sm text-gray-400">Active Alerts</h3>
                <p className="text-4xl font-bold mt-2 text-red-500">3</p>
              </div>
              <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                <h3 className="text-sm text-gray-400">Throughput</h3>
                <p className="text-4xl font-bold mt-2 text-green-500">156</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="col-span-2 bg-gray-800 p-6 rounded-lg shadow-lg h-[600px]">
                <h3 className="text-xl font-bold mb-4">Live Train Map</h3>
                <NetworkMap />
              </div>
              <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                <h3 className="text-xl font-bold mb-4">AI Recommendations</h3>
                <ul className="space-y-4">
                  <li className="bg-gray-900 p-4 rounded-lg">
                    <p className="text-sm text-yellow-400">Warning: Crossing conflict</p>
                    <p className="text-xs text-gray-300 mt-1">Express train E456 and Freight train F123 approaching same junction.</p>
                  </li>
                  <li className="bg-gray-900 p-4 rounded-lg">
                    <p className="text-sm text-red-500">High: Platform overlap</p>
                    <p className="text-xs text-gray-300 mt-1">Local train L789 scheduled for occupied platform.</p>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      );
    }
    
