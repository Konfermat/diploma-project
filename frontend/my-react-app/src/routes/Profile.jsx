import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Изменили redirect на useNavigate
import { jwtDecode } from 'jwt-decode'; // Импортируем декодер токена
import API from '../api/axios'; 

export default function Profile() {
  const { id } = useParams(); // Извлекаем id из URL
  const navigate = useNavigate(); // Хук для редиректов
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('access_token');

    // 1. ПРОВЕРКА НАЛИЧИЯ ТОКЕНА
    if (!token) {
      navigate('/login', { replace: true });
      return;
    }

    // 2. ОБРАБОТКА МАРШРУТА БЕЗ ID (/profile)
    if (!id) {
      try {
        const decoded = jwtDecode(token);
        const myId = decoded.user_id; // Достаем ID текущего пользователя
        navigate(`/profile/${myId}/`, { replace: true }); // Перенаправляем на /profile/{id}/
      } catch (err) {
        console.error("Ошибка декодирования токена:", err);
        localStorage.clear();
        navigate('/login', { replace: true });
      }
      return; // Останавливаем выполнение текущего эффекта, так как пошел редирект
    }

    // Сбрасываем старые данные и ошибку при смене id
    setUser(null);
    setError('');

    // 3. ЗАПРОС К БЭКЕНДУ ДЛЯ КОНКРЕТНОГО ID
    API.get(`user_detail/${id}/`)
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
        
        // Очистку токенов при 401 ошибке за нас делает Axios Interceptor!
      });
  }, [id, navigate]); // Эффект сработает при изменении id или функции навигации

  // 1. Состояние загрузки (или ожидания редиректа)
  if (!id || (!user && !error)) {
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
