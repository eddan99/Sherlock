const BASE_URL = "http://localhost:8000"

export async function uploadDocument(file) {
  const formData = new FormData()
  formData.append("file", file)
  const res = await fetch(`${BASE_URL}/documents`, {
    method: "POST",
    body: formData,
  })
  return res.json()
}

export async function queryDocument(question) {
  const res = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  })
  return res.json()
}
