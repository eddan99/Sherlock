import { useState } from 'react'
import './App.css'
import ChatInput from './components/ChatInput'
import ChatMessage from './components/ChatMessage'

function App() {
  const [messages, setMessages] = useState([])

  return (
    <>
      {messages.map((msg, i) => (
        <ChatMessage key={i} role={msg.role} text={msg.text} />
      ))}
      <ChatInput messages={messages} setMessages={setMessages} />
    </>
  )
}

export default App
