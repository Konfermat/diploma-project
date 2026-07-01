import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000', 
  headers: {
    'Content-Type': 'application/json',
  },
});

// 1. Ваш текущий перехватчик запросов (оставляем как есть, он отличный)
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// 2. НОВЫЙ перехватчик ответов: ловит 401 ошибку и обновляет токен
API.interceptors.response.use(
  (response) => response, // Если запрос успешный, просто возвращаем ответ
  async (error) => {
    const originalRequest = error.config;

    // Если бэкенд ответил 401 (Unauthorized) и мы еще не пробовали повторить этот запрос
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Защита от бесконечного цикла запросов

      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          // Делаем запрос к Django на обновление токена. 
          // Важно: используем чистый axios, а не API, чтобы не зациклить интерцепторы.
          const response = await axios.post('http://127.0.0', {
            refresh: refreshToken,
          });

          // Сохраняем новый access токен
          const newAccessToken = response.data.access;
          localStorage.setItem('access_token', newAccessToken);

          // Обновляем заголовок в упавшем запросе и перезапускаем его
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return API(originalRequest); 
          
        } catch (refreshError) {
          // Если refresh токен тоже протух (например, юзер не заходил неделю)
          console.error('Refresh-токен недействителен. Разлогиниваем...');
          handleLogout();
          return Promise.reject(refreshError);
        }
      } else {
        // Если рефреш-токена вообще нет
        handleLogout();
      }
    }

    return Promise.reject(error);
  }
);

// Функция для очистки данных и перенаправления на авторизацию
function handleLogout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  window.location.href = '/login'; // Автоматический редирект на страницу входа
}

export default API;
