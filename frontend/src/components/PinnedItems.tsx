import React, { useEffect, useState } from 'react';
import {
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  CircularProgress,
  Alert,
  Box,
  Divider,
} from '@mui/material';
import { client } from '../services/apiService';
import type { components } from '../services/api';

const PinnedItems = ({ isAdmin } : { isAdmin: boolean }) => {
  const [pinnedEvents, setPinnedEvents] = useState<components['schemas']['Event'][]>([]);
  const [pinnedLocations, setPinnedLocations] = useState<components['schemas']['Location'][]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPinnedItems = async () => {
    setLoading(true);
    setError(null);
    try {
      const events = await client.GET('/admin/pinned_events', {});
      const locations = await client.GET('/admin/pinned_locations', {});
      setPinnedEvents(events.data?.pinned_events ?? []);
      setPinnedLocations(locations.data?.pinned_locations ?? []);
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error('Error fetching pinned items:', err);
      setError('Failed to load pinned items.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPinnedItems();
  }, []);

  const unpinEvent = async (id: string) => {
    await client.DELETE('/admin/unpin_event/{event_id}', { params: { path: { event_id: id }} });
    fetchPinnedItems();
  };

  const unpinLocation = async (id: string) => {
    await client.DELETE('/admin/unpin_location/{location_id}', { params: { path: { location_id: id }} });
    fetchPinnedItems();
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Pinned Items
      </Typography>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      )}
      {error && (
        <Alert severity="error" sx={{ mt: 4 }}>
          {error}
        </Alert>
      )}

      {!loading && !error && (
        <>
          {/* Pinned Events Section */}
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
              Pinned Events
            </Typography>
            <Divider sx={{ mb: 2 }} />
            {pinnedEvents.length > 0 ? (
              <Grid container spacing={3}>
                {pinnedEvents.map((event) => (
                  <Grid item xs={12} sm={6} md={4} key={event.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {event.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {event.location}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                          {event.description ?? 'No description available.'}
                        </Typography>
                        {event.date && (
                          <Typography
                            variant="body2"
                            color="textSecondary"
                            sx={{ mt: 1 }}
                          >
                            {new Date(event.date).toLocaleDateString('en-US', {
                              weekday: 'short',
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric',
                            })}
                          </Typography>
                        )}
                      </CardContent>
                      {isAdmin && (
                        <CardActions>
                          <Button
                            size="small"
                            color="error"
                            onClick={async () => unpinEvent(event.id)}
                          >
                            Unpin
                          </Button>
                        </CardActions>
                      )}
                    </Card>
                  </Grid>
                ))}
              </Grid>
            ) : (
              <Typography variant="body2" color="textSecondary">
                No pinned events.
              </Typography>
            )}
          </Box>

          {/* Pinned Locations Section */}
          <Box sx={{ mt: 6 }}>
            <Typography variant="h5" gutterBottom>
              Pinned Locations
            </Typography>
            <Divider sx={{ mb: 2 }} />
            {pinnedLocations.length > 0 ? (
              <Grid container spacing={3}>
                {pinnedLocations.map((location) => (
                  <Grid item xs={12} sm={6} md={4} key={location.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {location.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {location.city}
                        </Typography>
                        {location.amenity && (
                          <Typography
                            variant="body2"
                            color="textSecondary"
                            sx={{ mt: 1 }}
                          >
                            Amenity: {location.amenity}
                          </Typography>
                        )}
                      </CardContent>
                      {isAdmin && (
                        <CardActions>
                          <Button
                            size="small"
                            color="error"
                            onClick={async () => unpinLocation(location.id)}
                          >
                            Unpin
                          </Button>
                        </CardActions>
                      )}
                    </Card>
                  </Grid>
                ))}
              </Grid>
            ) : (
              <Typography variant="body2" color="textSecondary">
                No pinned locations.
              </Typography>
            )}
          </Box>
        </>
      )}
    </Box>
  );
};

export default PinnedItems;
