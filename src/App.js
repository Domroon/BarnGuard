import React, { useState, useEffect } from "react"
import logo from "./logo.svg"
import "./App.css"

function App() {
  const [videos, setVideos] = useState("None")

  useEffect(() => {
    fetch("http://172.21.160.1:5000/api/videos")
      .then((res) => res.json())
      .then((data) => {
        setVideos(data[1].date)
      })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>Here are the videos: </p>
        <p>{videos}</p>
        <a className="App-link" href="https://reactjs.org" target="_blank" rel="noopener noreferrer">
          Learn React
        </a>
      </header>
    </div>
  )
}

export default App
