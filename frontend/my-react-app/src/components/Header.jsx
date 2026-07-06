import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

export default function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return !!localStorage.getItem('access_token');
  });
  
  const [isDarkTheme, setIsDarkTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme === 'dark'; 
  });

  // Новое состояние для бургер-меню
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navigate = useNavigate();
  const location = useLocation();

  // Начальный размер шрифта в пикселях (для базового текста)
  const [fontSize, setFontSize] = useState(16);
  // Функции для увеличения и уменьшения с границами (чтобы текст не стал слишком мелким или огромным)
  const increaseFont = () => setFontSize(prev => Math.min(prev + 2, 28)); // Максимум 28px
  const decreaseFont = () => setFontSize(prev => Math.max(prev - 2, 12)); // Минимум 12px
  const resetFont = () => setFontSize(16); // Сброс на стандартный


  // Закрываем бургер-меню при смене страницы
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
    setIsMenuOpen(false); 
  }, [location]);

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
    setIsMenuOpen(false); // Закрываем меню после выбора темы
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token'); 
    setIsLoggedIn(false);
    setIsMenuOpen(false);
    alert('Вы вышли из системы');
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="header-logo">
        <Link to="/"><h3>Уроки и Тесты</h3></Link>
      </div>

      {/* Кнопка бургера (активна только на мобильных/при масштабе) */}
      <button 
        className={`burger-toggle ${isMenuOpen ? 'open' : ''}`} 
        onClick={() => setIsMenuOpen(!isMenuOpen)}
        aria-label="Открыть меню"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Общая обертка для навигации, которая будет трансформироваться */}
      <div className={`header-menu ${isMenuOpen ? 'active' : ''}`}>
        
        <nav className="nav-group">
          <button className="nav-btn register-btn" onClick={toggleTheme}>
            {isDarkTheme ? 'Светлый стиль' : 'Темный стиль'}
          </button>
          <Link to="/lessons" className="body nav-btn register-btn">Уроки</Link>
        </nav>

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
        
      </div>
    </header>
  );
}
