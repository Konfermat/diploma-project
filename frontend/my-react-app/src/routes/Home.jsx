import { useState } from "react";

export default function Home() {
  // Начальный размер шрифта в пикселях (для базового текста)
  const [fontSize, setFontSize] = useState(16);
  // Функции для увеличения и уменьшения с границами (чтобы текст не стал слишком мелким или огромным)
  const increaseFont = () => setFontSize(prev => Math.min(prev + 2, 28)); // Максимум 28px
  const decreaseFont = () => setFontSize(prev => Math.max(prev - 2, 12)); // Минимум 12px
  const resetFont = () => setFontSize(16); // Сброс на стандартный

  return (
    <>
      {/* Передаем текущий размер шрифта через инлайн-стиль как CSS-переменную */}
      <div className="text-box" style={{ '--dynamic-font-size': `${fontSize}px` }}>
        
        {/* Панель управления шрифтом */}
        <div className="font-controls">
          <button onClick={decreaseFont} className="font-btn" title="Уменьшить шрифт">а-</button>
          <button onClick={resetFont} className="font-btn" title="Сбросить размер">Сбросить</button>
          <button onClick={increaseFont} className="font-btn" title="Увеличить шрифт">А+</button>
          <span className="font-indicator">{fontSize}px</span>
        </div>

        <h2>What is Lorem Ipsum?</h2>
        <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride Printing Library in London, took a 1914 Cicero translation and scrambled it to make dummy text for Letraset's Body Type sheets. It has survived not only many decades, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised thanks to these sheets and more recently with desktop publishing software like Aldus PageMaker and Microsoft Word including versions of Lorem Ipsum.</p>
        
        <h2>Why do we use it?</h2>
        <p>It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).</p>
      </div>
    </>
  );
}
