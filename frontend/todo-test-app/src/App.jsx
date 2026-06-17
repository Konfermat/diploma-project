import { useState, useEffect } from 'react';

function App() {
  // Создаем состояние для хранения данных курса
  const [course, setCourse] = useState(null);
  // Состояние для отображения процесса загрузки
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Функция для отправки запроса к Django API
    fetch('http://127.0.0.1:8000/courses/') // Укажи свой URL эндпоинта
      .then((response) => response.json())
      .then((data) => {
        setCourse(data); // Сохраняем данные в стейт
        setLoading(false); // Выключаем режим загрузки
      })
      .catch((error) => {
        console.error('Ошибка при получении данных:', error);
        setLoading(false);
      });
  }, []); // Пустой массив означает, что запрос выполнится 1 раз при монтировании

  // Если данные еще загружаются, показываем заглушку
  if (loading) {
    return <h1>Загрузка...</h1>;
  }

  // Если данные не пришли (например, ошибка сервера)
  if (!course) {
    return <h1>Ошибка загрузки курса</h1>;
  }

  return (
    <>
      <header>
        <h3>Заголовок</h3>
      </header>

      <div className="content-header">
        {/* Подставляем данные из API динамически */}
        <h1 id="course-title">{course[0].title}</h1>
        <p className="course-desc" id="course-desc">
          {course[0].description}
        </p>
      </div>
    </>
  );
}

export default App;
