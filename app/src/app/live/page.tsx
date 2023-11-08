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
    return webcamRef.current.getScreenshot()
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
    if (!text.endsWith(char)) {
      text = text + char
      setText(text)
    }
  }

  async function cameraLoop() {
    while (true) {
      console.log("a")
      await sleep(1000)
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
      <div className="flex h-full items-center justify-center">
        <div className="mx-auto flex h-full w-[80%] justify-around border-2 bg-white p-10">
          {started ? (
            <CameraComponent setText={setText} />
          ) : (
            <div className="flex items-center justify-start">
              <button
                onClick={() => {
                  setStarted(true)
                }}
                className="rounded-xl border-2 border-solid border-[#d1d5db] bg-gray-100 p-10 text-4xl font-semibold text-[#11111c]"
              >
                {/* Start Recording */}
                <h2 className="pb-4 font-semibold underline">
                  General Instructions
                </h2>
                <ul className="py-4">
                  <li className="py-2">
                    <p className="text-2xl font-medium text-black">
                      • Click on the "Start Recording" button
                    </p>
                  </li>
                  <li className="py-2">
                    <p className="text-2xl font-medium text-black">
                      • After you click, you will be asked to <br /> give the
                      permission for accessing <br />
                      the camera, allow it.
                    </p>
                  </li>
                  <li className="py-2">
                    <p className="text-2xl font-medium text-black">
                      • Keep your hand inside the camera frame
                    </p>
                  </li>
                </ul>
              </button>
            </div>
          )}
        </div>
      </div>
      <div className="m-10 flex h-1/5 flex-row items-center justify-center border-2 border-solid bg-gray-50 font-['Poppins'] text-2xl text-gray-800">
        <p>
          {!text && "The predictions will appear here"}
          {text && "•"} {text}
        </p>
      </div>
    </div>
  )
}
