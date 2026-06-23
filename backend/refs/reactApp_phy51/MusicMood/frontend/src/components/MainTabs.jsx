import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Container, Row, Col, Tabs, Tab, Alert, Spinner, Form, Button, InputGroup } from 'react-bootstrap';
import { FaSearch } from 'react-icons/fa';
import TrackCard from './TrackCard';
import * as api from '../api/api'; // Импортируем всё как объект api

const MOODS = [
    { key: 'joy', name: 'Радость', icon: '😀' },
    { key: 'calm', name: 'Спокойствие', icon: '🧘‍♂️' },
    { key: 'energy', name: 'Энергия', icon: '💃' },
    { key: 'sadness', name: 'Грусть', icon: '😪' },
    { key: 'focus', name: 'Фокус', icon: '🧠' },
];

const MainTabs = ({ onTrackPlay, setCurrentPlaylist }) => {
    const [key, setKey] = useState('mood');
    const [tracks, setTracks] = useState([]);
    const [favorites, setFavorites] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [activeMood, setActiveMood] = useState('joy');
    const [timeOfDay, setTimeOfDay] = useState('');

    const favIds = useMemo(() => new Set(favorites.map(f => f.track_id)), [favorites]);

    const loadContent = useCallback(async (targetKey, mood = activeMood) => {
        setLoading(true);
        setError(null);
        try {
            const favRes = await api.getFavorites();
            setFavorites(favRes.data);

            let res;
            if (targetKey === 'mood') res = await api.getTracksByMood(mood);
            else if (targetKey === 'collection') {
                res = await api.getTracksByTime();
                setTimeOfDay(res.data.time_of_day);
                res.data = res.data.tracks;
            }
            else if (targetKey === 'favorites') res = { data: favRes.data };

            const data = res.data || [];
            setTracks(data);
            setCurrentPlaylist(data);
        } catch (e) {
            setError('Ошибка загрузки данных');
        } finally {
            setLoading(false);
        }
    }, [activeMood, setCurrentPlaylist]);

    useEffect(() => {
        if (key !== 'results') loadContent(key);
    }, [key, loadContent]);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!searchQuery.trim()) return;
        setLoading(true);
        try {
            const res = await api.searchTracks(searchQuery);
            setTracks(res.data);
            setCurrentPlaylist(res.data);
            setKey('results');
        } catch { setError('Ошибка поиска'); }
        finally { setLoading(false); }
    };

    const handleToggleFavorite = async (track) => {
        try {
            const isFav = favIds.has(track.track_id);
            if (isFav) {
                await api.removeFavorite(track.track_id);
                setFavorites(prev => prev.filter(f => f.track_id !== track.track_id));
                if (key === 'favorites') setTracks(prev => prev.filter(t => t.track_id !== track.track_id));
            } else {
                const res = await api.addFavorites(track);
                setFavorites(prev => [res.data, ...prev]);
            }
        } catch { alert("Ошибка обновления избранного"); }
    };

    const renderContent = () => {
        if (loading) return <div className='text-center py-5'><Spinner animation='border' variant='primary' /></div>;
        if (error) return <Alert variant='danger'>{error}</Alert>;

        return (
            <Row className='mt-4 g-3 justify-content-center'>
                {tracks.length > 0 ? tracks.map(track => (
                    <TrackCard
                        key={track.track_id}
                        track={track}
                        isFavorite={favIds.has(track.track_id)}
                        onPlay={onTrackPlay}
                        onToggleFavorite={handleToggleFavorite}
                    />
                )) : <Alert variant='info' className="text-center w-100">Треков пока нет.</Alert>}
            </Row>
        );
    };

    return (
        <Container className='py-4'>
            <h2 className='text-center mb-4 text-primary'>MusicMood</h2>

            <Form onSubmit={handleSearch} className='mb-4'>
                <InputGroup size='lg'>
                    <Form.Control placeholder='Найти трек...' value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
                    <Button variant='primary' type='submit'><FaSearch /></Button>
                </InputGroup>
            </Form>

            {key === 'results' ? (
                <div className="mb-3">
                    <Button variant='link' onClick={() => setKey('mood')}>← Назад</Button>
                    <h4>Результаты для: {searchQuery}</h4>
                    {renderContent()}
                </div>
            ) : (
                <Tabs activeKey={key} onSelect={setKey} className='nav-pills justify-content-center'>
                    <Tab eventKey='mood' title='По настроению'>
                        <div className='d-flex justify-content-center gap-2 my-3 flex-wrap'>
                            {MOODS.map(m => (
                                <Button key={m.key} variant={activeMood === m.key ? 'primary' : 'outline-primary'}
                                    onClick={() => { setActiveMood(m.key); loadContent('mood', m.key); }} className='rounded-pill'>
                                    {m.icon} {m.name}
                                </Button>
                            ))}
                        </div>
                    </Tab>
                    <Tab eventKey='collection' title='Подборка'>
                        <h4 className='text-center text-muted my-3'>
                            Сейчас: {timeOfDay === 'morning' ? 'Утро' : timeOfDay === 'afternoon' ? 'День' : 'Вечер'}
                        </h4>
                    </Tab>
                    <Tab eventKey='favorites' title='Избранное' />
                </Tabs>
            )}
            {key !== 'results' && renderContent()}
        </Container>
    );
};

export default MainTabs;