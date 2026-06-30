import { Navigate } from 'react-router-dom';

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem('access_token');
  
  // Если токена нет в localStorage, отправляем на логин
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Если токен есть, рендерим защищенный компонент
  return children;
}
