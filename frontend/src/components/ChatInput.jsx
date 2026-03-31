
import { useState, useRef } from "react"
import { uploadDocument, queryDocument } from "../api"
import { Paperclip } from "lucide-react"

function ChatInput({ setMessages, setUploadStatus }) {
  const [input, setInput] = useState("")
  const fileInputReference = useRef(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isUploading, setIsUploading] = useState(false)

  async function handleSend() {
    if (!input.trim() || isLoading || isUploading) return
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
    setIsUploading(true)
    setUploadStatus("Uploading...")
    await uploadDocument(file)
    setUploadStatus(`${file.name} uploaded`)
    setIsUploading(false)
  }

  return (
    <div className="chat-input-wrapper">
      <input type="file" accept=".pdf" onChange={handleFileUpload} ref={fileInputReference} hidden />
      <button className="upload-btn" onClick={() => fileInputReference.current.click()}><Paperclip size={20} />
</button>
      <input
        className="chat-input"
        type="text"
        placeholder="ask sherlock..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && !isUploading && handleSend()}
      />
      <button className="send-btn" onClick={handleSend} disabled={isLoading || isUploading}>
        {isLoading ? "..." : "Send"}
      </button>
    </div>
  )
}

export default ChatInput