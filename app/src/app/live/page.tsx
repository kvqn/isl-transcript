"use client"

import React from "react"
import Webcam from "react-webcam"

export default function Page() {
  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user",
  }

  const webcamRef = React.useRef(null)
  const capture = React.useCallback(() => {
    if (!webcamRef.current) return
    if (!webcamRef.current.getScreenshot) return
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
    console.log(await result.json())
  }

  return (
    <>
      <Webcam
        audio={false}
        height={720}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={1280}
        videoConstraints={videoConstraints}
      />
      <button onClick={action}>Capture photo</button>
    </>
  )
}
