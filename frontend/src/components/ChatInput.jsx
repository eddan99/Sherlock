
import { useState } from "react"

function ChatInput({ onSend, onFileUpload }) {
  const [input, setInput] = useState("")

    function handleSend() {
    if (!input.trim()) return
    onSend(input)
    setInput("")
  }

  return (
    <div>
      <input type="file" accept=".pdf" onChange={onFileUpload} />
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  )
}

export default ChatInput