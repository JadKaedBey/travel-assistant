import React, { useState } from 'react';
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
import { client } from '../services/apiService';

const PinForm = ({ onRefresh } : { onRefresh: () => void }) => {
  const [pinType, setPinType] = useState('event');
  const [name, setName] = useState('');
  const [city, setCity] = useState('');
  const [description, setDescription] = useState('');
  const [date, setDate] = useState('');
  const [category, setCategory] = useState('');
  const [amenity, setAmenity] = useState('cafe');
  const [lat, setLat] = useState('');
  const [lon, setLon] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const id = Date.now().toString(); // Generate unique ID

    if (pinType === 'event') {
      const eventData = {
        id,
        name,
        location: city,
        description,
        date: date ? new Date(date).toISOString() : null,
        category,
        priority: 0,
        pinned: true,
      };
      await client.POST('/admin/pin_event', { body: eventData });
    } else {
      const latFloat = parseFloat(lat);
      const lonFloat = parseFloat(lon);
      if (isNaN(latFloat) || isNaN(lonFloat)) {
        // eslint-disable-next-line no-alert
        alert('Please enter valid latitude and longitude coordinates.');
        return;
      }
      const locationData = {
        id,
        name,
        city,
        amenity,
        lat: latFloat,
        lon: lonFloat,
        description,
      };
      await client.POST('/admin/pin_location', { body: locationData });
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
        borderColor: 'white',
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
          onChange={(e) => { setPinType(e.target.value); }}
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
            onChange={(e) => { setName(e.target.value); }}
            fullWidth
            required
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="City"
            value={city}
            onChange={(e) => { setCity(e.target.value); }}
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
              onChange={(e) => { setDescription(e.target.value); }}
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
              onChange={(e) => { setDate(e.target.value); }}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Category"
              value={category}
              onChange={(e) => { setCategory(e.target.value); }}
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
              onChange={(e) => { setAmenity(e.target.value); }}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              label="Latitude"
              value={lat}
              onChange={(e) => { setLat(e.target.value); }}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              label="Longitude"
              value={lon}
              onChange={(e) => { setLon(e.target.value); }}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Description"
              value={description}
              onChange={(e) => { setDescription(e.target.value); }}
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
