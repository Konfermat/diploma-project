import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

// Компонент Карточка Товара
// name, price - пропсы (входящие данные), только для чтения
// useEffect(function, [список зависимостей])
function ProductCard({ name, price }){
  const [count, setCount] = useState(0);
  useEffect( ()=>{
    if (count > 0){
      console.log(`Товар ${name} обновлен в корзине. Всего ${count} шт`);
    }
  }, [count]);
  
  // обработчик клика
  const handleAdd = () => {
    setCount(count + 1);
  };
  return (
    <div style={{ border: '1px solid $ccc', padding: '20px', 
    borderRadius: '10px' }}>
      <h2>{name}</h2>
      <p>Цена: {price} руб</p>
      <p>В корзине <strong>{count}</strong> шт.</p>
      <button onClick={handleAdd} >
        Добавить в корзину
      </button>
      {count > 0 && <button onClick={() => setCount(0)}>Сбросить</button>}
    </div>
  );
}


function App() {

  return (
    <>
      <h1>Пробный компонетн</h1>
      <ProductCard name='SmartPhone' price={150000} />
      <ProductCard name='Watch' price={20000} />
    </>
  );
}

export default App
