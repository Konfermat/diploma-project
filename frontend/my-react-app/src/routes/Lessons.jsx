import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import API from '../api/axios'; // Твой настроенный экземпляр Axios
import Header from '../components/Header';

export default function Lessons() {
  const [lessons, setLessons] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        setIsLoading(true);
        setError('');
        
        const response = await API.get('lessons/');
        setLessons(response.data);
      } catch (err) {
        console.error(err);
        if (err.response) {
          setError(`Ошибка сервера: ${err.response.status}`);
        } else {
          setError('Не удалось подключиться к серверу.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchLessons();
  }, []);

  return (
    <>
      <div className="text-box">
        <h2>Доступные уроки</h2>

        {isLoading && <p>Загрузка списка уроков...</p>}

        {error && <div className="error-summary">{error}</div>}

        {!isLoading && !error && (
          <div className="lessons-list">
            {lessons.length === 0 ? (
              <p className="text-left">На данный момент уроков нет.</p>
            ) : (
              lessons.map((lesson) => (
                <div key={lesson.id} className="lesson-card">
                  <div className="lesson-content">
                    <h3>{lesson.title}</h3>
                    {lesson.description && <p>{lesson.description}</p>}
                  </div>
                  
                  <Link to={`/lesson/${lesson.id}`} className="nav-btn register-btn btn-nowrap">
                    Перейти
                  </Link>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </>
  );
}
