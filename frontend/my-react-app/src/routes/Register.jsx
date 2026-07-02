import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Добавили useNavigate для редиректа после регистрации
import API from '../api/axios'; // Импортируем твой настроенный инстанс Axios

export default function Register() {
  const navigate = useNavigate(); // Инициализируем хук навигации
  
  const [data, setData] = useState({ 
    username: '', 
    first_name: '', 
    last_name: '', 
    email: '', 
    password: '', 
    confirmPassword: '' 
  });
  
  const [errors, setErrors] = useState({});
  const [serverErrors, setServerErrors] = useState({}); // Состояние для ошибок валидации от Django

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
    const { name, value } = e.target;
    const updatedData = { ...data, [name]: value };
    setData(updatedData);
    validate(name, value, updatedData);
    
    // Очищаем ошибку бэкенда для конкретного поля при начале ввода нового значения
    if (serverErrors[name]) {
      setServerErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  // Метод отправки данных на бэкенд
  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerErrors({}); // Сбрасываем старые серверные ошибки перед новым запросом

    // Формируем чистый объект для DRF (без confirmPassword)
    const { confirmPassword, ...payload } = data;

    try {
      // 1. Делаем POST-запрос на твой эндпоинт регистрации (замени 'register/' на свой урл, если он другой)
      const response = await API.post('register/', payload);

      if (response.status === 201 || response.status === 200) {
        alert('Регистрация прошла успешно! Теперь вы можете войти.');
        navigate('/login'); // Перенаправляем пользователя на страницу логина
      }
    } catch (err) {
      console.error('Ошибка регистрации:', err);
      
      // 2. Обрабатываем ошибки валидации от Django REST Framework
      if (err.response && err.response.data) {
        // DRF обычно возвращает ошибки в формате { поле: ["Текст ошибки"] }
        setServerErrors(err.response.data);
      } else {
        // На случай падения самого сервера
        setServerErrors({ non_field_errors: 'Произошла непредвиденная ошибка на сервере. Попробуйте позже.' });
      }
    }
  };

  const isFormInvalid = 
    !data.username || !data.email || !data.password || !data.confirmPassword ||
    Object.values(errors).some(error => error !== '');

  return (
    <div className="container">
      <h2>Регистрация</h2>
      
      {/* Вывод общих ошибок бэкенда, не привязанных к конкретным полям */}
      {serverErrors.non_field_errors && (
        <div className="error-summary" style={{color: 'red', marginBottom: '10px'}}>
          {serverErrors.non_field_errors}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div>
          <input type="text" name="username" placeholder="Имя пользователя (логин)" value={data.username} onChange={handleChange} required />
          {errors.username && <span className="error-text">{errors.username}</span>}
          {/* Ошибка уникальности юзернейма от Django */}
          {serverErrors.username && <span className="error-text" style={{color: 'red'}}>{serverErrors.username}</span>}
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
          {/* Ошибка уникальности email от Django */}
          {serverErrors.email && <span className="error-text" style={{color: 'red'}}>{serverErrors.email}</span>}
        </div>

        <div>
          <input type="password" name="password" placeholder="Пароль" value={data.password} onChange={handleChange} required />
          {errors.password && <span className="error-text">{errors.password}</span>}
          {serverErrors.password && <span className="error-text" style={{color: 'red'}}>{serverErrors.password}</span>}
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

