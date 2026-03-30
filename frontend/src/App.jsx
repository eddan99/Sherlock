import { useState } from 'react'  
import './App.css'
import ChatInput from './components/ChatInput'
import ChatMessage from './components/ChatMessage'

function App() {
  const [messages, setMessages] = useState([])

  return (
    <>
      <ChatMessage />
      <ChatInput />

    </>
  )
}

export default App
