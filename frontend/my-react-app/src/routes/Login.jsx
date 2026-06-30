import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import API from '../api/axios'; 

export default function Login() {
  const navigate = useNavigate(); 
  
  const [data, setData] = useState({ username: '', password: '' });
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState(''); 

  const validate = (name, value) => {
    let errorText = '';

    if (name === 'username' && value.trim().length < 3) {
      errorText = 'Имя пользователя слишком короткое';
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError(''); 

    try {
      const response = await API.post('token/', {
        username: data.username,
        password: data.password
      });

      if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        
        navigate('/profile');
      }
    } catch (err) {
      console.error(err);
      if (err.response && err.response.status === 401) {
        setServerError('Неверное имя пользователя или пароль');
      } else {
        setServerError('Произошла ошибка на сервере. Попробуйте позже.');
      }
    }
  };

  const isFormInvalid = 
    !data.username || !data.password || 
    Object.values(errors).some(error => error !== '');

  return (
    <div className="container">
      <h2>Вход в аккаунт</h2>
      
      {serverError && <div className="error-summary" style={{color: 'red', marginBottom: '10px'}}>{serverError}</div>}
      
      <form onSubmit={handleSubmit}>
        <div>
          <input type="text" name="username" placeholder="Имя пользователя" value={data.username} onChange={handleChange} required />
          {errors.username && <span className="error-text">{errors.username}</span>}
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
