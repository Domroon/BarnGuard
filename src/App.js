import React, { useState, useEffect } from "react"

import Videos from "./components/Videos"
import Login from "./components/Login"
import Register from "./components/Register"
import ReducedHeader from "./components/ReducedHeader"
import Footer from "./components/Footer"

function App() {
  const [selectedDate, handleDateChange] = useState(new Date())
  const [videos, setVideos] = useState("None")
  const [state, setState] = useState({ startDate: null, endDate: null, focusedInput: null })
  const [endDate, setEndDate] = useState(null)
  const [focusedInput, setFocusedInput] = useState(null)

  useEffect(() => {
    fetch("/api/videos")
      .then((res) => res.json())
      .then((data) => {
        setVideos(data[1].date)
      })
  }, [])

  return (
    <>
      <ReducedHeader />
      <Login />
      <Footer />
    </>
  )
}

export default App
