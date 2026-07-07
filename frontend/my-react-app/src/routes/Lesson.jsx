import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import API from '../api/axios'; // Твой настроенный экземпляр Axios

export default function Lesson() {
  // Извлекаем id, который указан в URL (например, /lesson/5)
  const { id } = useParams();
  
  const [lesson, setLesson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchLessonDetail = async () => {
      try {
        setIsLoading(true);
        setError('');
        
        // Отправляем GET-запрос к эндпоинту Django для одного урока (со слэшем в конце для DRF)
        const response = await API.get(`lessons/${id}/`);
        setLesson(response.data);
      } catch (err) {
        console.error(err);
        if (err.response) {
          setError(`Ошибка загрузки урока: ${err.response.status}`);
        } else {
          setError('Не удалось подключиться к серверу.');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchLessonDetail();
  }, [id]); // Перезапускать эффект, если id изменится

  return (
    <div className="text-box">
      {/* Кнопка возврата к списку всех уроков */}
      <Link to="/lessons" className="link-btn text-left" style={{ display: 'block', marginBottom: '20px' }}>
        ← Назад к списку уроков
      </Link>

      {isLoading && <p>Загрузка содержимого урока...</p>}

      {error && <div className="error-summary">{error}</div>}

      {!isLoading && !error && lesson && (
        <div className="lesson-detail">
          <h2 style={{ textAlign: 'left', marginTop: '0', color: 'var(--text-primary)' }}>
            {lesson.title}
          </h2>
          
          {/* Контент урока (текст, видео или задания, в зависимости от твоей Django-модели) */}
          <div className="lesson-text-content" style={{ color: 'var(--text-primary)', marginTop: '20px', lineHeight: '1.6' }}>
            {lesson.content ? (
              <p className="text-left">{lesson.content}</p>
            ) : (
              <p className="text-left" style={{ fontStyle: 'italic', color: 'var(--text-secondary)' }}>
                У этого урока пока нет текстового содержимого.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
