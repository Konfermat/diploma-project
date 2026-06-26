import { useState } from 'react';
import { Link } from 'react-router-dom'


export default function Register({ onSwitch }) {
  const [Data, setData] = useState({ name: '', email: '', password: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData({ ...Data, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Данные регистрации:', Data);
    alert('Успешная регистрация!');
  };

  return (
    <>
      <div className="container">
        <h2>Регистрация</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" name="name" placeholder="Имя" value={Data.name} onChange={handleChange} required />
          <input type="email" name="email" placeholder="Email" value={Data.email} onChange={handleChange} required />
          <input type="password" name="password" placeholder="Пароль" value={Data.password} onChange={handleChange} required />
          <button type="submit">Создать аккаунт</button>
        </form>
        <p>Уже есть аккаунт? <Link to="/login" className="link-btn">Войти</Link></p>
      </div>
      </>
  );
}
