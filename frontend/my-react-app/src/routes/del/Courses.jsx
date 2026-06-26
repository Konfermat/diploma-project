import Header from '../components/Header.jsx';
import { useState, useEffect } from 'react';
import api from '../data/api.js';

export default function Courses(props) {
  // Изначально стейт пуст
  const [courseTitles, setCourseTitles] = useState([]);
  const [loading, setLoading] = useState(true);
  // Запрашиваем данные у DRF при монтировании компонента 
  useEffect(() => {
    api.get('course_titles/') 
      .then(response => {
        setCourseTitles(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Ошибка получения данных", error);
        setLoading(false);
      });
  }, []); 

  // Состояние загрузки, пока данные летят от DRF
  if (loading) {
    return <p>Загрузка курсов...</p>;
  }

  return (
    <>
      <Header />
      <div className="content">
        <h3>Список доступных курсов</h3>
        
        {courseTitles.length === 0 ? (
          <p className="no-courses">Курсов пока нет. Загляните позже!</p>
        ) : (
          <ul className="list" id="list">
            {courseTitles.map((course, index) => (
              <li key={index} className="list">
                {course}
              </li>
            ))}
          </ul>
        )}

      </div>
    </>
  );  
}

