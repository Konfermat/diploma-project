import { useState, useEffect } from 'react';
// 1. Исправили импорт (указали путь ./ и вытащили конкретную переменную)
import { API_ENDPOINTS } from './api'; 

function App() {
  // Меняем имя переменной на множественное число, так как это список (массив)
  const [courses, setCourses] = useState([]); 
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(API_ENDPOINTS.COURSES_LIST)
      .then((response) => response.json())
      .then((data) => {
        setCourses(data); // Сохраняем полученный массив курсов
        setLoading(false); 
      })
      .catch((error) => {
        console.error('Ошибка при получении данных:', error);
        setLoading(false);
      });
  }, []); 

  if (loading) {
    return <h1>Загрузка...</h1>;
  }

  // Проверяем, что массив не пустой, прежде чем брать первый элемент
  if (courses.length === 0) {
    return <h1>Курсы не найдены или произошла ошибка сервера</h1>;
  }

  return (
    <>
      {console.log(courses[1].title)}
      {console.log(courses[1].title)}
      <header>
        <h3>Заголовок</h3>
      </header>

      <div className="content-header">
        <h1 id="course-title">{courses[1].title}</h1>
        <p className="course-desc" id="course-desc">
          {courses[1].description}
        </p>
      </div>
    </>
  );
}

export default App;