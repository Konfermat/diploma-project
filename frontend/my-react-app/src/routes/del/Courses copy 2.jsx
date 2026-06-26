import Header from '../components/Header.jsx'
import { useState } from 'react';

function Courses(props) {

  return (
    <>
      <Header />
      <div className="content-header">
        <h1 id="course-title">Поколение Python</h1>
        <p className="course-desc" id="course-desc">В курсе рассказывается об основных типах данных, конструкциях и принципах структурного программирования языка Python. Курс содержит теорию в формате текстовых конспектов и более 500 задач с автоматизированной проверкой.</p>
      </div>
      
      <div className="container">
        <div className="sidebar">
          <h3>Список доступных курсов</h3>
          <ul className="step-list" id="step-list">
            <li className="step-item active">Урок 1: Введение и основы</li>
          </ul>
        </div>
      </div>
     
    </>
  );  
}
export default Courses;