import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom'; // Добавили useLocation

export default function Header() {
  // Инициализация авторизации: проверяем, есть ли токен в localStorage
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return !!localStorage.getItem('access_token'); // Вернет true, если токен есть, и false, если его нет
  });
  
  const [isDarkTheme, setIsDarkTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme === 'dark'; 
  });

  const navigate = useNavigate();
  const location = useLocation(); // Слушаем изменение страниц

  // Эффект для синхронизации авторизации при переходах по страницам
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
  }, [location]); // Срабатывает каждый раз, когда пользователь переходит на другую страницу (например, после успешного логина)

  // Эффект для темы оформления
  useEffect(() => {
    if (isDarkTheme) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDarkTheme]);

  const toggleTheme = () => {
    setIsDarkTheme(prev => !prev);
  };

  const handleLogout = () => {
    // ОЧИСТКА: Удаляем токены DRF из локального хранилища
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token'); 
    
    setIsLoggedIn(false);
    alert('Вы вышли из системы');
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="header-logo">
        <Link to="/"><h3>MyDRFApp</h3></Link>
      </div>

      <button className="theme-toggle" onClick={toggleTheme}>
        {isDarkTheme ? 'Светлый стиль' : 'Темный стиль'}
      </button>

      <nav className="header-nav">
        {isLoggedIn ? (
          <div className="nav-group">
            <Link to="/profile" className="nav-btn profile-btn">Личный кабинет</Link>
            <button onClick={handleLogout} className="nav-btn logout-btn">Выйти</button>
          </div>
        ) : (
          <div className="nav-group">
            <Link to="/login" className="nav-btn login-btn">Войти</Link>
            <Link to="/register" className="nav-btn register-btn">Регистрация</Link>
          </div>
        )}
      </nav>
    </header>
  );
}
