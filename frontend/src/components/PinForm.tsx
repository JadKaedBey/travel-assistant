import React, { useState } from 'react';
import axios from 'axios';
import {
  TextField,
  Select,
  MenuItem,
  Button,
  Grid,
  Typography,
  Box,
  InputLabel,
  FormControl,
} from '@mui/material';

const PinForm = ({ onRefresh }) => {
  const [pinType, setPinType] = useState('event');
  const [name, setName] = useState('');
  const [city, setCity] = useState('');
  const [description, setDescription] = useState('');
  const [date, setDate] = useState('');
  const [category, setCategory] = useState('');
  const [amenity, setAmenity] = useState('cafe');
  const [lat, setLat] = useState('');
  const [lon, setLon] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const id = Date.now().toString(); // Generate unique ID
    let data;

    if (pinType === 'event') {
      data = {
        id,
        name,
        location: city,
        description,
        date: date ? new Date(date).toISOString() : null,
        category,
        priority: 0,
        pinned: true,
      };
      await axios.post('/admin/pin_event', data, {
        baseURL: import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000',
      });
    } else {
      if (isNaN(lat) || isNaN(lon)) {
        alert('Please enter valid latitude and longitude coordinates.');
        return;
      }
      data = {
        id,
        name,
        city,
        amenity,
        lat: parseFloat(lat),
        lon: parseFloat(lon),
        description,
      };
      await axios.post('/admin/pin_location', data, {
        baseURL: import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000',
      });
    }

    onRefresh();
    setName('');
    setCity('');
    setDescription('');
    setDate('');
    setCategory('');
    setAmenity('cafe');
    setLat('');
    setLon('');
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        p: 4,
        backgroundColor: 'black',
        boxShadow: 3,
        borderRadius: 2,
        borderColor: "white",
        maxWidth: 600,
        mx: 'auto',
      }}
    >
      <Typography variant="h5" gutterBottom>
        Pin a {pinType}
      </Typography>

      {/* Select Pin Type */}
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="pin-type-label">Select Type</InputLabel>
        <Select
          labelId="pin-type-label"
          value={pinType}
          onChange={(e) => setPinType(e.target.value)}
          fullWidth
        >
          <MenuItem value="event">Event</MenuItem>
          <MenuItem value="location">Location</MenuItem>
        </Select>
      </FormControl>

      {/* Shared Fields */}
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TextField
            label="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            fullWidth
            required
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="City"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            fullWidth
            required
          />
        </Grid>
      </Grid>

      {/* Event-Specific Fields */}
      {pinType === 'event' && (
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12}>
            <TextField
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              fullWidth
              multiline
              rows={3}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              fullWidth
            />
          </Grid>
        </Grid>
      )}

      {/* Location-Specific Fields */}
      {pinType === 'location' && (
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12}>
            <TextField
              label="Amenity Type"
              value={amenity}
              onChange={(e) => setAmenity(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              label="Latitude"
              value={lat}
              onChange={(e) => setLat(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              label="Longitude"
              value={lon}
              onChange={(e) => setLon(e.target.value)}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              fullWidth
              multiline
              rows={3}
            />
          </Grid>
        </Grid>
      )}

      {/* Submit Button */}
      <Button
        type="submit"
        variant="contained"
        color="primary"
        sx={{ mt: 3, width: '100%' }}
      >
        Pin {pinType}
      </Button>
    </Box>
  );
};

export default PinForm;
