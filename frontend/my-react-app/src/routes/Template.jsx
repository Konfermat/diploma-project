import Header from '../components/Header.jsx'
import { useState } from 'react'

export default function Template(props) {
  const [isOpen, setIsOpen] = useState(false);  
  return (
    <>
      <div className="container">
      </div>
    </>
  );  
}