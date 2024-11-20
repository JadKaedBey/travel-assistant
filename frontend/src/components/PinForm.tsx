// Src/components/PinForm.js

import React, { useState } from 'react';
import axios from 'axios';

const PinForm = ({ onRefresh }) => {
  const [pinType, setPinType] = useState('event');
  const [name, setName] = useState('');
  const [city, setCity] = useState('');
  const [amenity, setAmenity] = useState('cafe');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = { id: Date.now().toString(), name, location: city, amenity };

    if (pinType === 'event') {
      await axios.post('/admin/pin_event', data, {
        baseURL: import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'
      });
    } else {
      await axios.post('/admin/pin_location', data, {
        baseURL: import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'
      });
    }

    onRefresh();
    setName('');
    setCity('');
    setAmenity('cafe');
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-gray-100 rounded">
      <h3 className="text-lg font-bold mb-2">Pin an {pinType}</h3>
      <select
        onChange={(e) => { setPinType(e.target.value); }}
        value={pinType}
        className="mb-2 p-2 border rounded w-full"
      >
        <option value="event">Event</option>
        <option value="location">Location</option>
      </select>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => { setName(e.target.value); }}
        className="mb-2 p-2 border rounded w-full"
      />
      <input
        type="text"
        placeholder="City"
        value={city}
        onChange={(e) => { setCity(e.target.value); }}
        className="mb-2 p-2 border rounded w-full"
      />
      {pinType === 'location' && (
        <input
          type="text"
          placeholder="Amenity Type"
          value={amenity}
          onChange={(e) => { setAmenity(e.target.value); }}
          className="mb-2 p-2 border rounded w-full"
        />
      )}
      <button
        type="submit"
        className="w-full px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 cursor-pointer"
      >
        Pin {pinType}
      </button>
    </form>
  );
};

export default PinForm;
