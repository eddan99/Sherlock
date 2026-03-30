
import { useState, useRef } from "react"

function ChatInput({ onSend, onFileUpload }) {
  const [input, setInput] = useState("")
  const fileRef = useRef(null)

  function handleSend() {
    if (!input.trim()) return
    onSend(input)
    setInput("")
  }

  return (
    <div>
      <input type="file" accept=".pdf" onChange={onFileUpload} ref={fileRef} hidden />
      <button onClick={() => fileRef.current.click()}>+</button>
      <input
        type="text"
        placeholder="Ask Sherlock"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  )
}

export default ChatInput