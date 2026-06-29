import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Login() {
  // Переменные приведены к стандарту camelCase
  const [data, setData] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});

  const validate = (name, value) => {
    let errorText = '';

    if (name === 'email' && !/\S+@\S+\.\S+/.test(value)) {
      errorText = 'Неверный формат email';
    }
    if (name === 'password' && value.length < 6) {
      errorText = 'Пароль слишком короткий';
    }

    setErrors((prev) => ({ ...prev, [name]: errorText }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    const updatedData = { ...data, [name]: value };
    setData(updatedData);
    validate(name, value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Данные для входа:', data);
    alert('Вы успешно вошли!');
  };

  const isFormInvalid = 
    !data.email || !data.password || 
    Object.values(errors).some(error => error !== '');

  return (
    <div className="container">
      <h2>Вход в аккаунт</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input type="email" name="email" placeholder="Email" value={data.email} onChange={handleChange} required />
          {errors.email && <span className="error-text">{errors.email}</span>}
        </div>

        <div>
          <input type="password" name="password" placeholder="Пароль" value={data.password} onChange={handleChange} required />
          {errors.password && <span className="error-text">{errors.password}</span>}
        </div>

        <button type="submit" disabled={isFormInvalid}>Войти</button>
      </form>
      <p>Нет аккаунта? <Link to="/register" className="link-btn">Зарегистрироваться</Link></p>
    </div>
  );
}
