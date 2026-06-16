import Todo from "./components/Todo";
import Form from "./components/Form";
import FilterButton from "./components/FilterButton";


function App(props) {

  const taskList = props.tasks?.map((task) => (
    <Todo
      id={task.id}
      name={task.name}
      completed={task.completed}
      key={task.id} />
  ));

  return (
    <>
      <div className="todoapp stack-large">
        <h1>TodoMatic</h1>
        <Form />
        <div className="filters btn-group stack-exception">
          <FilterButton />
          <FilterButton />
          <FilterButton />
          <button type="button" className="btn toggle-btn" aria-pressed="false">
            <span className="visually-hidden">Показать </span>
            <span>активные</span>
            <span className="visually-hidden"> задачи</span>
          </button>
          <button type="button" className="btn toggle-btn" aria-pressed="false">
            <span className="visually-hidden">Показать </span>
            <span>завершенные</span>
            <span className="visually-hidden"> задачи</span>
          </button>
        </div>
        <h2 id="list-heading">осталось три задачи</h2>
        <ul
          role="list"
          className="todo-list stack-large stack-exception"
          aria-labelledby="list-heading">
          {taskList}
        </ul>
      </div>
    </>
  );
}

export default App;
