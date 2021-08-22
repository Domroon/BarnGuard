import React, { useState, useEffect } from "react"
import logo from "./logo.svg"
import "./App.css"
import { Button, Row, Col, Form, Container } from "react-bootstrap"
import CardExample from "./CardExample"
import BootstrapExample from "./BootstrapExample"

function App() {
  const [videos, setVideos] = useState("None")

  useEffect(() => {
    fetch("/api/videos")
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
        <Button variant="success">Test</Button>
        <BootstrapExample />
        <CardExample />
      </header>
    </div>
  )
}

export default App
