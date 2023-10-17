export async function POST(request: Request) {
  const { file } = await request.json()

  const formData = new FormData()
  formData.append("file", file)

  const result = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    body: formData,
  })

  const json = await result.json()

  console.log(json)

  return new Response(JSON.stringify(json), {
    headers: {
      "content-type": "application/json; charset=UTF-8",
    },
  })
}
