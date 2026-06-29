import { BrowserRouter, Routes, Route } from "react-router-dom"
import { useState, useEffect } from 'react'

import Template from './routes/Template.jsx'
import Register from './routes/Register.jsx'
import Profile from './routes/Profile.jsx'
import Login from './routes/Login.jsx'
import Test from './routes/Test.jsx'

import Header from './components/Header.jsx'
import './App.css'

export default function App() {
  // 1. Инициализируем состояние. Проверяем, есть ли уже сохраненная тема в браузере.
  // Если там написано 'true', то включаем темную тему (true), иначе светлую (false).
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme === 'dark';
  });

  // 2. Этот useEffect теперь делает два дела:
  // - Переключает CSS-класс на теге <html>
  // - Записывает актуальный выбор пользователя в localStorage
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark'); // Сохраняем строку 'dark'
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light'); // Сохраняем строку 'light'
    }
  }, [isDarkMode]);

  return (
    <BrowserRouter>
      <Header isDarkMode={isDarkMode} onToggleTheme={() => setIsDarkMode(!isDarkMode)} />

      <Routes>
        <Route path="/" element={ <Template /> } />
        <Route path="/template" element={ <Template /> } />
        <Route path="/register" element={ <Register /> } />
        <Route path="/login" element={ <Login /> } />
        <Route path="/test" element={ <Test /> } />
        <Route path="/profile" element={ <Profile /> } />
      </Routes>
    </BrowserRouter>
  );
}
