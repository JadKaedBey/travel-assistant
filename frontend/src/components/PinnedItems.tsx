// Src/components/PinnedItems.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PinnedItems = ({ isAdmin } : { isAdmin: boolean }) => {
  const [pinnedEvents, setPinnedEvents] = useState([]);
  const [pinnedLocations, setPinnedLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPinnedItems = async () => {
    setLoading(true);
    setError(null);
    try {
      const events = await axios.get('/admin/pinned_events', {
        baseURL: import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'
      });
      const locations = await axios.get('/admin/pinned_locations', {
        baseURL: import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'
      });
      setPinnedEvents(events.data.pinned_events || []);
      setPinnedLocations(locations.data.pinned_locations || []);
    } catch (error) {
      console.error('Error fetching pinned items:', error);
      setError('Failed to load pinned items.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPinnedItems();
  }, []);

  const unpinEvent = async (id) => {
    await axios.delete(`/admin/unpin_event/${id}`, {
      baseURL: import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'
    });
    fetchPinnedItems();
  };

  const unpinLocation = async (id) => {
    await axios.delete(`/admin/unpin_location/${id}`, {
      baseURL: import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'
    });
    fetchPinnedItems();
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Pinned Items</h2>
            
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
            
      {!loading && !error && (
        <>
          {/* Pinned Events Section */}
          <section className="mb-6">
            <h3 className="text-lg font-semibold mb-2">Pinned Events</h3>
            {pinnedEvents.length > 0 ? (
              <ul className="space-y-2">
                {pinnedEvents.map((event) => (
                  <li key={event.id} className="p-4 bg-gray-100 rounded flex justify-between items-center">
                    <div>
                      <p className="font-medium">{event.name}</p>
                      <p className="text-sm text-gray-500">{event.city}</p>
                    </div>
                    {isAdmin && (
                      <button
                        onClick={async () => unpinEvent(event.id)}
                        className="px-2 py-1 text-red-500 border border-red-500 rounded hover:bg-red-500 hover:text-white"
                      >
                                                Unpin
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No pinned events.</p>
            )}
          </section>

          {/* Pinned Locations Section */}
          <section>
            <h3 className="text-lg font-semibold mb-2">Pinned Locations</h3>
            {pinnedLocations.length > 0 ? (
              <ul className="space-y-2">
                {pinnedLocations.map((location) => (
                  <li key={location.id} className="p-4 bg-gray-100 rounded flex justify-between items-center">
                    <div>
                      <p className="font-medium">{location.name}</p>
                      <p className="text-sm text-gray-500">{location.city}</p>
                      <p className="text-xs text-gray-400">{location.amenity}</p>
                    </div>
                    {isAdmin && (
                      <button
                        onClick={async () => unpinLocation(location.id)}
                        className="px-2 py-1 text-red-500 border border-red-500 rounded hover:bg-red-500 hover:text-white"
                      >
                                                Unpin
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No pinned locations.</p>
            )}
          </section>
        </>
      )}
    </div>
  );
};

export default PinnedItems;
