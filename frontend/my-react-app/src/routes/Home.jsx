import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="text-box">
      {/* Главный заголовок */}
      <h1>Добро пожаловать на обучающую платформу! 👋</h1>
      
      {/* Краткое описание */}
      <p className="text-left" style={{ fontSize: '1.15rem', lineHeight: '1.6', marginBottom: '30px' }}>
        Здесь собран интерактивный лекционный материал, разбитый на удобные части, и практические тесты для закрепления знаний. Изучайте темы в своём темпе, настраивайте шрифты для комфортного чтения и проверяйте свои силы.
      </p>

      {/* Список возможностей в твоем стиле */}
      <div style={{ marginBottom: '30px' }}>
        <h3 className="text-left">Что вас ждет на платформе:</h3>
        <ul>
          <li className="text-left" style={{ marginBottom: '10px' }}>
            <strong>Структурированные уроки</strong> — каждая тема разбита на пошаговые подразделы для легкого усвоения.
          </li>
          <li className="text-left" style={{ marginBottom: '10px' }}>
            <strong>Интерактивные тесты</strong> — проверяйте свои знания сразу после прочтения теоретического материала.
          </li>
          <li className="text-left" style={{ marginBottom: '10px' }}>
            <strong>Кастомизация текста</strong> — меняйте шрифты прямо внутри уроков для максимального удобства.
          </li>
        </ul>
      </div>

      {/* Главная кнопка перехода к урокам */}
      <div style={{ marginTop: '20px' }}>
        <Link to="/lessons" className="link-btn" style={{ display: 'inline-block' }}>
          Перейти к списку уроков →
        </Link>
      </div>
    </div>
  );
}
