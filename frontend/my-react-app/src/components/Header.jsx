import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function Header() {
  // Временное состояние: true — вошел на сайт, false — гость.
  // Переключи вручную на true/false, чтобы проверить, как меняются кнопки.
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  
  const navigate = useNavigate();

  const handleLogout = () => {
    // Здесь в будущем будет вызов функции очистки токенов DRF
    setIsLoggedIn(false);
    alert('Вы вышли из системы');
    navigate('/login'); // Перенаправляем на страницу входа
  };

  return (
    <header className="header">
      <div className="header-logo">
        <Link to="/"><h3>MyDRFApp</h3></Link>
      </div>

      <nav className="header-nav">
        {isLoggedIn ? (
          // Интерфейс для авторизованного пользователя
          <div className="nav-group">
            <Link to="/profile" className="nav-btn profile-btn">Личный кабинет</Link>
            <button onClick={handleLogout} className="nav-btn logout-btn">Выйти</button>
          </div>
        ) : (
          // Интерфейс для гостя
          <div className="nav-group">
            <Link to="/login" className="nav-btn login-btn">Войти</Link>
            <Link to="/register" className="nav-btn register-btn">Регистрация</Link>
          </div>
        )}
      </nav>
    </header>
  );
}
