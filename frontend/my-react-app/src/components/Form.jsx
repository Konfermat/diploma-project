function Form() {
  return (
    <>
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
    </>
  );
}

export default Form;