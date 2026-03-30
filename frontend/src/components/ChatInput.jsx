
import { useState, useRef } from "react"
import { uploadDocument, queryDocument } from "../api"

function ChatInput({ messages, setMessages }) {
  const [input, setInput] = useState("")
  const fileRef = useRef(null)
  const [isLoading, setIsLoading] = useState(false)

  async function handleSend() {
    if (!input.trim() || isLoading) return
    setMessages(prev => [...prev, { role: "user", text: input }, { role: "assistant", text: "..." }])
    setInput("")
    setIsLoading(true)
    const data = await queryDocument(input)
    setMessages(prev => {
      const updated = [...prev]
      updated[updated.length - 1] = { role: "assistant", text: data.answer }
      return updated
    })
    setIsLoading(false)
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
      <button onClick={handleSend} disabled={isLoading}>
        {isLoading ? "..." : "Send"}
      </button>
    </div>
  )
}

export default ChatInput