import { useState } from 'react';
import { Link } from 'react-router-dom'



export default function Login({ onSwitch }) {
  const [Data, setData] = useState({ email: '', password: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData({ ...Data, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Данные для входа:', Data);
    alert('Вы успешно вошли!');
  };

  return (
    <>
      <div className="container">
        <h2>Вход в аккаунт</h2>
        <form onSubmit={handleSubmit}>
          <input type="email" name="email" placeholder="Email" value={Data.email} onChange={handleChange} required />
          <input type="password" name="password" placeholder="Пароль" value={Data.password} onChange={handleChange} required />
          <button type="submit">Войти</button>

        </form>
        <p>Нет аккаунта? <Link to="/register" className="link-btn">Зарегистрироваться</Link></p>
      </div>
    </>    
  );
}
