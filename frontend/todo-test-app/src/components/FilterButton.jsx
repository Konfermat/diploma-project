function FilterButton(props) {
  return (
    <>
      <button type="button" className="btn toggle-btn" aria-pressed="true">
        <span className="visually-hidden">Показать </span>
        <span>все</span>
        <span className="visually-hidden"> задачи</span>
      </button>
    </>
  );
}

export default FilterButton;