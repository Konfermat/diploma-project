import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Register() {
  // Добавили first_name и last_name в состояние. Поля необязательные, поэтому в начале пустые строки
  const [data, setData] = useState({ 
    username: '', 
    first_name: '', 
    last_name: '', 
    email: '', 
    password: '', 
    confirmPassword: '' 
  });
  const [errors, setErrors] = useState({});

  // Первый аргумент — это имя поля (name), а не конкретно username
  const validate = (name, value, allData) => {
    let errorText = '';

    if (name === 'username' && value.trim().length < 3) {
      errorText = 'Имя пользователя должно быть не короче 3 символов';
    }
    if (name === 'email' && !/\S+@\S+\.\S+/.test(value)) {
      errorText = 'Введите корректный email';
    }
    if (name === 'password') {
      if (value.length < 6) {
        errorText = 'Пароль должен быть не менее 6 символов';
      }
      if (allData.confirmPassword && value !== allData.confirmPassword) {
        setErrors((prev) => ({ ...prev, confirmPassword: 'Пароли не совпадают' }));
      } else if (allData.confirmPassword && value === allData.confirmPassword) {
        setErrors((prev) => ({ ...prev, confirmPassword: '' }));
      }
    }
    if (name === 'confirmPassword' && value !== allData.password) {
      errorText = 'Пароли не совпадают';
    }

    setErrors((prev) => ({ ...prev, [name]: errorText }));
  };

  const handleChange = (e) => {
    // ВАЖНО: деструктурируем именно 'name' из e.target, так как это имя HTML-атрибута
    const { name, value } = e.target;
    const updatedData = { ...data, [name]: value };
    setData(updatedData);
    validate(name, value, updatedData);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Данные для отправки в DRF:', data);
    alert('Успешная регистрация!');
  };

  // Кнопка заблокирована, если обязательные поля DRF пусты или есть ошибки.
  // first_name и last_name в AbstractUser по умолчанию могут быть пустыми, поэтому здесь их не проверяем на обязательность
  const isFormInvalid = 
    !data.username || !data.email || !data.password || !data.confirmPassword ||
    Object.values(errors).some(error => error !== '');

  return (
    <div className="container">
      <h2>Регистрация</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input type="text" name="username" placeholder="Имя пользователя (логин)" value={data.username} onChange={handleChange} required />
          {errors.username && <span className="error-text">{errors.username}</span>}
        </div>

        <div>
          <input type="text" name="first_name" placeholder="Имя" value={data.first_name} onChange={handleChange} />
          {errors.first_name && <span className="error-text">{errors.first_name}</span>}
        </div>

        <div>
          <input type="text" name="last_name" placeholder="Фамилия" value={data.last_name} onChange={handleChange} />
          {errors.last_name && <span className="error-text">{errors.last_name}</span>}
        </div>

        <div>
          <input type="email" name="email" placeholder="Email" value={data.email} onChange={handleChange} required />
          {errors.email && <span className="error-text">{errors.email}</span>}
        </div>

        <div>
          <input type="password" name="password" placeholder="Пароль" value={data.password} onChange={handleChange} required />
          {errors.password && <span className="error-text">{errors.password}</span>}
        </div>

        <div>
          <input type="password" name="confirmPassword" placeholder="Повторите пароль" value={data.confirmPassword} onChange={handleChange} required />
          {errors.confirmPassword && <span className="error-text">{errors.confirmPassword}</span>}
        </div>

        <button type="submit" disabled={isFormInvalid}>Создать аккаунт</button>
      </form>
      <p>Уже есть аккаунт? <Link to="/login" className="link-btn">Войти</Link></p>
    </div>
  );
}
