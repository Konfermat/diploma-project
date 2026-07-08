import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import API from '../api/axios'; // Твой настроенный экземпляр Axios

export default function Lesson() {
  // Извлекаем id, который указан в URL (например, /lesson/5)
  const { id } = useParams();
  
  const [lesson, setLesson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

    // Начальный размер шрифта в пикселях (для базового текста)
  const [fontSize, setFontSize] = useState(16);
  // Функции для увеличения и уменьшения с границами (чтобы текст не стал слишком мелким или огромным)
  const increaseFont = () => setFontSize(prev => Math.min(prev + 2, 28)); // Максимум 28px
  const decreaseFont = () => setFontSize(prev => Math.max(prev - 2, 12)); // Минимум 12px
  const resetFont = () => setFontSize(16); // Сброс на стандартный

  useEffect(() => {
    const fetchLessonDetail = async () => {
      try {
        setIsLoading(true);
        setError('');
        
        // Отправляем GET-запрос к эндпоинту Django для одного урока (со слэшем в конце для DRF)
        const response = await API.get(`lesson/${id}/`);
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
    <div className="text-box" style={{ '--dynamic-font-size': `${fontSize}px` }}>
      
      {/* Кнопка возврата к списку всех уроков */}
      <Link to="/lessons" className="link-btn text-left" style={{ display: 'block', marginBottom: '20px' }}>
        ← Назад к списку уроков
      </Link>
      
        
      {/* Панель управления шрифтом */}
      <div className="font-controls">
        <button onClick={decreaseFont} className="font-btn" title="Уменьшить шрифт">а-</button>
        <button onClick={resetFont} className="font-btn" title="Сбросить размер">Сбросить</button>
        <button onClick={increaseFont} className="font-btn" title="Увеличить шрифт">А+</button>
        <span className="font-indicator">{fontSize}px</span>
      </div>      

      {isLoading && <p>Загрузка содержимого урока...</p>}

      {error && <div className="error-summary">{error}</div>}

      {!isLoading && !error && lesson && (
        <div className="lesson-detail">
          <h2 style={{ textAlign: 'left', marginTop: '0', color: 'var(--text-primary)' }}>
            {lesson.title}
          </h2>
          
          {/* Контент урока, разбитый по частям (parts) */}
          <div className="lesson-text-content" style={{ color: 'var(--text-primary)', marginTop: '20px', lineHeight: '1.6' }}>
            {lesson.parts && lesson.parts.length > 0 ? (
              lesson.parts
                .sort((a, b) => a.order - b.order) // Сортируем части по порядку, если бэкенд не отсортировал
                .map((part) => (
                  <div key={part.id} className="lesson-part" style={{ marginBottom: '30px' }}>
                    
                    {/* Название подраздела (например: Что такое Lorem Ipsum?) */}
                    <h3 className="text-left" style={{ color: 'var(--text-primary)', marginBottom: '10px' }}>
                      {part.title}
                    </h3>

                    {/* Вывод текстов внутри этого подраздела */}
                    {part.texts && part.texts.length > 0 ? (
                      part.texts
                        .sort((a, b) => a.order - b.order) // Сортируем параграфы по порядку
                        .map((textItem) => (
                          <p key={textItem.id} className="text-left" style={{ marginBottom: '15px' }}>
                            {textItem.lesson_material}
                          </p>
                        ))
                    ) : (
                      <p className="text-left" style={{ fontStyle: 'italic', color: 'var(--text-secondary)' }}>
                        В этой части пока нет текста.
                      </p>
                    )}

                    {/* Место для тестов (если массив tests не пустой) */}
                    {part.tests && part.tests.length > 0 && (
                      <div className="part-tests" style={{ marginTop: '15px', padding: '10px', background: '#f9f9f9', borderRadius: '5px' }}>
                        <strong className="text-left" style={{ display: 'block', marginBottom: '5px' }}>Доступные тесты:</strong>
                        {/* Здесь будет логика отображения тестов, когда они появятся в базе данных */}
                        <p className="text-left" style={{ fontSize: '14px' }}>У этого подраздела есть практические задания.</p>
                      </div>
                    )}

                  </div>
                ))
            ) : (
              <p className="text-left" style={{ fontStyle: 'italic', color: 'var(--text-secondary)' }}>
                У этого урока пока нет разделов с содержимым.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
