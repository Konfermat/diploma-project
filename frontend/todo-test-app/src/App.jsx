import Todo from "./components/Todo.jsx"
import Home from "./components/Home.jsx"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import './App.css'
import { useState } from "react"

// Даже если это просто начальные данные, их лучше вынести в отдельный файл (например, src/data/todoData.js), чтобы не загромаждать App.jsx.
const DATA = [
  { id: "todo-0", name: "Eat", completed: true },
  { id: "todo-1", name: "Sleep", completed: false },
  { id: "todo-2", name: "Repeat", completed: false },
];


function App() {
  const [tasks, setTasks] = useState(DATA);

  return (

    <BrowserRouter>
      <Routes>
        {/* <Route path="/" element={ <Home tasks={DATA} /> } /> */}
        <Route path="/" element={ <Home tasks={tasks} setTasks={setTasks} /> } />
        <Route path="/todo" element={ <Todo /> } />
      </Routes>
    </BrowserRouter>


  );
}

export default App;