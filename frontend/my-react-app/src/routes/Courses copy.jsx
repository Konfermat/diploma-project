import Header from '../components/Header.jsx'
import { useState } from 'react'

function Courses(props) {
    // Развертывание теста
  const [isOpen, setIsOpen] = useState(false);  
  return (
    <>

      <Header />

      <div className="content-header">
        <h1 id="course-title">Поколение Python</h1>
        <p className="course-desc" id="course-desc">В курсе рассказывается об основных типах данных, конструкциях и принципах структурного программирования языка Python. Курс содержит теорию в формате текстовых конспектов и более 500 задач с автоматизированной проверкой.</p>
      </div>

      <div className="container">
        <aside className="sidebar">
          <h3>Уроки курса</h3>
          <ul className="step-list" id="step-list">
            <li className="step-item active">Урок 1: Введение и основы</li>
          </ul>
        </aside>

        <main className="content" id="lesson-content">
          <div className="element theory-block">
            <h3>Теория к уроку</h3><br/><br/>
            В этом уроке мы разберем базовые концепции. Python — это высокоуровневый язык программирования, который отлично подходит для новичков благодаря простому синтаксису.
          </div>
          
          <div>
            <button onClick={() => setIsOpen(!isOpen)}>
              {isOpen ? 'Свернуть' : 'Развернуть'}
            </button>
            
            <div className="" style={{
              display: 'grid',
              gridTemplateRows: isOpen ? '1fr' : '0fr',
              transition: 'grid-template-rows 0.3s ease-out',
              overflow: 'hidden'
            }}>
              <div style={{ minHeight: 0 }}>
                <p>Контент разворачивающегося блока.</p>
                <div className="element test-block">
                  Здесь сделаю пагинацию тестов?
                </div>
                <div className="element test-block">
                  <div className="test-question">Вопрос по теме урока: Сколько будет 5 + 3?</div>
                  <div className="options-list">
                    <label className="option-label">
                      <input type="radio" name="test-2" value="true" />
                      Правильный ответ (8)
                    </label>

                    <label className="option-label">
                      <input type="radio" name="test-2" value="false" />
                      Неправильный вариант А (7)
                    </label>

                    <label className="option-label">
                      <input type="radio" name="test-2" value="false" />
                      Неправильный вариант Б (9)
                    </label>
                  </div>
                  <button className="btn-check" onClick="checkAnswer(2)">Проверить ответ</button>
                  <div className="feedback" id="feedback-2"></div>
                </div>          
              </div>
            </div>
          </div> 

          <div className="element theory-block">
            <h3>Дополнительный материал</h3>
            Не забывайте практиковаться после каждого теста, чтобы закрепить материал на практике.
          </div>
        </main>
      </div>

     
    </>
  );  
}
export default Courses;