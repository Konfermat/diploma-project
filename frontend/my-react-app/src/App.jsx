import Template from './routes/Template.jsx'
import Courses from './routes/Courses.jsx'
import Header from './components/Header.jsx'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import { useState, useEffect } from 'react'
import './App.css'

function App() {
  // Развертывание теста
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <BrowserRouter>
        <Routes>
          {/* <Route path="/" element={ <Home tasks={DATA} /> } /> */}
          {/* <Route path="/" element={ <Home tasks={tasks} setTasks={setTasks} /> } /> */}
          {/* <Route path="/todo" element={ <Todo /> } /> */}
       
          <Route path="/" element={ <Header /> } />
          <Route path="/courses" element={ <Courses /> } />
          <Route path="/template" element={ <Template /> } />
        </Routes>
      </BrowserRouter>
    </>    
  );
}

export default App;