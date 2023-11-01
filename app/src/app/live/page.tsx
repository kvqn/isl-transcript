"use client"

import React, { useEffect, useState } from "react"
import Webcam from "react-webcam"

const sleep = (delay: number) =>
  new Promise((resolve) => setTimeout(resolve, delay))

type CameraComponentProps = {
  setText: React.Dispatch<React.SetStateAction<string>>
}

function CameraComponent(props: CameraComponentProps) {
  const { setText } = props

  let text = ""

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user",
  }

  const webcamRef = React.useRef(null)
  const capture = React.useCallback(() => {
    // @ts-ignore
    const imageSrc = webcamRef.current.getScreenshot()
    return imageSrc
  }, [webcamRef])

  const action = async () => {
    const result = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ file: capture() }),
    })

    const resp = await result.json()
    const char = resp.prediction
    if (char && !text.endsWith(char)) {
      text = text + char
      setText(text)
    }
  }

  async function cameraLoop() {
    while (true) {
      console.log("a")
      await sleep(50)
      console.log("b")
      await action()
    }
  }

  useEffect(() => {
    cameraLoop()
  }, [])

  return (
    <Webcam
      audio={false}
      ref={webcamRef}
      screenshotFormat="image/jpeg"
      videoConstraints={videoConstraints}
    />
  )
}

export default function Page() {
  const [text, setText] = useState("")
  const [started, setStarted] = useState(false)

  return (
    <div className="flex h-screen flex-col justify-evenly">
      <div className="flex h-4/5 w-full justify-around border-2 p-10">
        {started ? (
          <CameraComponent setText={setText} />
        ) : (
          <div className="flex items-center justify-center">
            <button
              onClick={() => {
                setStarted(true)
              }}
              className="bg-red-50"
            >
              Start
            </button>
          </div>
        )}
      </div>
      <div className="m-10 flex h-1/5 items-center justify-center border-2 border-solid font-['Poppins'] text-3xl">
        <p>{text}</p>
      </div>
    </div>
  )
}
