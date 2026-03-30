import { useState } from 'react'
import './App.css'
import ChatInput from './components/ChatInput'
import ChatMessage from './components/ChatMessage'

function App() {
  const [messages, setMessages] = useState([])

  return (
    <div className="app">
      <div className="messages">
        {messages.map((msg, i) => (
          <ChatMessage key={i} role={msg.role} text={msg.text} />
        ))}
      </div>
      <ChatInput setMessages={setMessages} />
    </div>
  )
}

export default App
