
import { useState, useRef } from "react"
import { uploadDocument, queryDocument } from "../api"

function ChatInput({ messages, setMessages }) {
  const [input, setInput] = useState("")
  const fileRef = useRef(null)

  async function handleSend() {
    if (!input.trim()) return
    setMessages(prev => [...prev, { role: "user", text: input }])
    setInput("")
    const data = await queryDocument(input)
    setMessages(prev => [...prev, { role: "assistant", text: data.answer }])
  }

    async function handleFileUpload(e) {
    const file = e.target.files[0]
    if (!file) return
    await uploadDocument(file)
    }

  return (
    <div>
      <input type="file" accept=".pdf" onChange={handleFileUpload} ref={fileRef} hidden />
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