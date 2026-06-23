import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
});

const DEFAULT_USER_ID = 'demo_user';

export const searchTracks = (query) => api.post('/tracks/', { query });
export const getTracksByMood = (mood) => api.post('/tracks/', { mood });
export const getTracksByTime = () => api.get('/tracks/mood/');
export const getFavorites = (userId = DEFAULT_USER_ID) => api.get('/favorites/', { params: { user_id: userId } });

export const addFavorites = (track) => api.post('/favorites/', {
    user_id: DEFAULT_USER_ID,
    ...track
});

export const removeFavorite = (track_id) => api.post('/favorites/delete/', {
    user_id: DEFAULT_USER_ID,
    track_id
});