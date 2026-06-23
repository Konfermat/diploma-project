import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Container, Row, Col, Card, Button, ProgressBar } from 'react-bootstrap';
import { FaPlay, FaPause, FaStepForward, FaStepBackward } from 'react-icons/fa';

const MusicPlayer = ({ currentTrack, currentPlaylist, onNext, onPrev }) => {
    const audioRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [time, setTime] = useState({ current: 0, total: 0 });

    // Универсальный переключатель
    const togglePlay = () => {
        const audio = audioRef.current;
        isPlaying ? audio.pause() : audio.play().catch(console.error);
        setIsPlaying(!isPlaying);
    };

    // Синхронизация при смене трека
    useEffect(() => {
        if (currentTrack && audioRef.current) {
            audioRef.current.src = currentTrack.audio_url;
            audioRef.current.play().then(() => setIsPlaying(true)).catch(console.error);
        }
    }, [currentTrack]);

    const formatTime = (s) => {
        if (!s || isNaN(s)) return "0:00";
        return `${Math.floor(s / 60)}:${Math.floor(s % 60).toString().padStart(2, '0')}`;
    };

    const handleProgress = (e) => {
        const { duration } = audioRef.current;
        const rect = e.currentTarget.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        if (Number.isFinite(duration)) audioRef.current.currentTime = pos * duration;
    };

    if (!currentTrack) return (
        <div className='fixed-bottom bg-light border-top py-3 text-center text-muted'>
            Выберите трек для начала прослушивания
        </div>
    );

    return (
        <div className='fixed-bottom bg-light border-top shadow-lg py-2'>
            <Container>
                <Row className='align-items-center'>
                    <Col xs={12} md={4} className='d-flex align-items-center mb-2 mb-md-0'>
                        <img src={currentTrack.album_image} alt="" style={{ width: 45, height: 45, borderRadius: 5, objectFit: 'cover' }} className='me-3' />
                        <div className="text-truncate">
                            <div className="fw-bold small">{currentTrack.name_track}</div>
                            <div className="text-muted extra-small" style={{ fontSize: '0.8rem' }}>{currentTrack.artist_name}</div>
                        </div>
                    </Col>

                    <Col xs={12} md={4} className='d-flex justify-content-center align-items-center mb-2 mb-md-0'>
                        <Button variant='link' className='text-dark' onClick={onPrev}><FaStepBackward /></Button>
                        <Button variant='primary' className='rounded-circle mx-3' onClick={togglePlay}>
                            {isPlaying ? <FaPause /> : <FaPlay />}
                        </Button>
                        <Button variant='link' className='text-dark' onClick={onNext}><FaStepForward /></Button>
                    </Col>

                    <Col xs={12} md={4}>
                        <div className='d-flex align-items-center gap-2'>
                            <small>{formatTime(time.current)}</small>
                            <div className='flex-grow-1 bg-secondary bg-opacity-25 rounded' style={{ height: 6, cursor: 'pointer' }} onClick={handleProgress}>
                                <div className="bg-primary h-100 rounded" style={{ width: `${(time.current / time.total) * 100 || 0}%` }} />
                            </div>
                            <small>{formatTime(time.total)}</small>
                        </div>
                    </Col>
                </Row>
                <audio
                    ref={audioRef}
                    onTimeUpdate={() => setTime(prev => ({ ...prev, current: audioRef.current.currentTime }))}
                    onLoadedMetadata={() => setTime(prev => ({ ...prev, total: audioRef.current.duration }))}
                    onEnded={onNext}
                />
            </Container>
        </div>
    );
};

export default MusicPlayer;