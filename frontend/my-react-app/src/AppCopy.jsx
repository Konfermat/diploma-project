
function App(props) {
  return (
    <>
      <div className="todoapp stack-large">

        <h1>TodoMatic</h1>

        <form>
          <h2 className="label-wrapper">
            <label htmlFor="new-todo-input" className="label__lg">
              Что планируется сделать?
            </label>
          </h2>
          <input
            type="text"
            id="new-todo-input"
            className="input input__lg"
            name="text"
            autoComplete="Off"
          />
          <button type="submit" className="btn btn_primary btn__lg">
            Добавить
          </button>

        </form>
        <div className="filters btn-group stack-exception">
          <button type="button" className="btn toggle-btn" aria-pressed="true">
            <span className="visually-hidden">Показать </span>
            <span>все</span>
            <span className="visually-hidden"> задачи</span>
          </button>
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
          <li className="todo stack-small">
            <div className="c-cb">
              <input id="todo-0" type="checkbox" defaultChecked />
              <label className="todo-label" htmlFor="todo-0">
                Поесть
              </label>
            </div>

            <div className="btn-group">
              <button type="button" className="btn">
                Изменить <span className="visually-hidden">Поесть</span>
              </button>
              <button type="button" className="btn btn__danger">
                Удалить <span className="visually-hidden">Поесть</span>
              </button>
            </div>
          </li>

          <li className="todo stack-small">
            <div className="c-cb">
              <input id="todo-1" type="checkbox" />
              <label className="todo-label" htmlFor="todo-1">
                Поспать
              </label>
            </div>

            <div className="btn-group">
              <button type="button" className="btn">
                Изменить <span className="visually-hidden">Поспать</span>
              </button>
              <button type="button" className="btn">
                Удалить <span className="visually-hidden">Поспать</span>
              </button>
            </div>
          </li>

          <li className="todo stack-small">
            <div className="c-cb">
              <input type="checkbox" id="todo-2" />
              <label className="todo-label" htmlFor="todo-2">
                Повторить
              </label>
            </div>

            <div className="btn-group">
              <button type="button" className="btn">
                Изменить <span className="visually-hidden">Повторить</span>
              </button>
              <button type="button" className="btn__danger">
                Удалить <span className="visually-hidden">Повторить</span>
              </button>            
            </div>
          </li>
        </ul>
      </div>
    </>
  );
}

export default App;
