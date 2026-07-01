import { useState, useEffect } from 'react';
import API from '../api/axios'; // Импортируем наш настроенный Axios-клиент
import { useParams } from 'react-router-dom';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    API.get('profile/')
      .then(response => {
        setUser(response.data); // Сохраняем пришедшие данные в состояние
      })
      .catch(err => {
        console.error("Не удалось загрузить профиль", err);
        setError('Ошибка загрузки данных профиля.');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        // костыль?
        setIsLoggedIn(false);       
      });
  }, []);

  // Пока запрос идет, показываем сообщение о загрузке
  if (!user && !error) {
    return <div className='container'><h2>Загрузка профиля...</h2></div>;
  }

  // Если произошла ошибка (например, протух токен)
  // TODO спроси про JWS токены
  if (error) {
    return <div className='container'><h2>{error}</h2></div>;
  }
  return (
    <div className='container'>
      <h2>Профиль аккаунта</h2>
      <p><strong>id пользователя:</strong> {user.id}</p>
      <p><strong>Имя пользователя:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email || 'Не указан'}</p>
      <p><strong>Статус (is_staff):</strong> {user.is_staff ? 'Администратор' : 'Студент'}</p>
      <p><strong>Дата регистрации:</strong> {user.date_joined}</p>
    </div>
  );
}
