import React from 'react';
import { Card, Button, Col } from 'react-bootstrap';
import { FaHeart, FaRegHeart, FaPlay } from 'react-icons/fa';

const TrackCard = ({ track, isFavorite, onPlay, onToggleFavorite }) => {
    const { name_track, artist_name, album_image } = track;
    return (
        <Col md={6} lg={4} className='mb-3'>
            <Card className='shadow-sm border-0 h-100 hover-shadow' onClick={() => onPlay(track)} style={{ cursor: 'pointer' }}>
                <Card.Body className='d-flex align-items-center p-2'>
                    <img src={album_image} alt="" style={{ width: 50, height: 50, borderRadius: 4 }} className="me-3" />
                    <div className='flex-grow-1 overflow-hidden'>
                        <div className='text-truncate fw-bold small'>{name_track}</div>
                        <div className='text-muted small text-truncate'>{artist_name}</div>
                    </div>
                    <div className="d-flex gap-2">
                        <Button variant='link' className='p-1 text-primary' onClick={(e) => { e.stopPropagation(); onPlay(track); }}>
                            <FaPlay size={14} />
                        </Button>
                        <Button variant='link' className={`p-1 ${isFavorite ? 'text-danger' : 'text-secondary'}`}
                                onClick={(e) => { e.stopPropagation(); onToggleFavorite(track); }}>
                            {isFavorite ? <FaHeart size={16} /> : <FaRegHeart size={16} />}
                        </Button>
                    </div>
                </Card.Body>
            </Card>
        </Col>
    );
};

export default TrackCard;