import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import API from '../api/axios'; // Наш настроенный Axios-клиент с интерцептором

export default function Profile() {
  const { id } = useParams(); // Извлекаем id из URL маршрута (/profile/:id)
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    // Сбрасываем старые данные и ошибку при смене id (например, перешли с profile/1 на profile/2)
    setUser(null);
    setError('');

    // Делаем динамический запрос к DRF, подставляя id
    API.get(`profile/${id}/`)
      .then(response => {
        setUser(response.data); // Сохраняем данные профиля
      })
      .catch(err => {
        console.error("Не удалось загрузить профиль:", err);
        
        // Обрабатываем разные типы ошибок от бэкенда
        if (err.response && err.response.status === 404) {
          setError('Профиль с таким ID не найден.');
        } else if (err.response && err.response.status === 403) {
          setError('У вас нет прав для просмотра этого профиля.');
        } else {
          setError('Ошибка загрузки данных профиля. Попробуйте позже.');
        }
        
        // Очистку токенов мы убрали — теперь её автоматически делает Axios Interceptor!
      });
  }, [id]); // useEffect сработает заново каждый раз, когда изменится id в URL

  // 1. Состояние загрузки
  if (!user && !error) {
    return (
      <div className='container'>
        <h2>Загрузка профиля...</h2>
      </div>
    );
  }

  // 2. Состояние ошибки
  if (error) {
    return (
      <div className='container'>
        <h2 style={{ color: 'red' }}>{error}</h2>
      </div>
    );
  }

  // 3. Успешный рендеринг профиля
  return (
    <div className='container'>
      <h2>Профиль аккаунта</h2>
      <p><strong>id пользователя:</strong> {user.id}</p>
      <p><strong>Имя пользователя:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email || 'Не указан'}</p>
      <p><strong>Статус (is_staff):</strong> {user.is_staff ? 'Администратор' : 'Студент'}</p>
      <p><strong>Дата регистрации:</strong> {new Date(user.date_joined).toLocaleDateString()}</p>
    </div>
  );
}
