import API from './axios';

// 1. Регистрация
export const register = async (username, email, password) => {
  const response = await API.post('register/', { username, email, password });
  return response.data;
};

// 2. Вход (Получение токенов)
export const login = async (username, password) => {
  const response = await API.post('token/', { username, password });
  if (response.data.access) {
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
  }
  return response.data;
};

// 3. Выход
export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};
