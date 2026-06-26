export default function Header({ isDarkMode, onToggleTheme }) {
  return (
    <header>
      <h3>Заголовок сайта</h3>
      
      {/* Кнопка вызывает функцию onToggleTheme, которая изменит состояние в App.jsx */}
      <button className="theme-toggle" onClick={onToggleTheme}>
        {isDarkMode ? 'Светлая тема' : 'Тёмная тема'}
      </button>  
    </header> 
  );
}
