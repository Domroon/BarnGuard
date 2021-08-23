import React, { useState, useEffect } from "react"
import logo from "./logo.svg"
import "./App.css"
import { Button } from "react-bootstrap"
import CardExample from "./CardExample"
import BootstrapExample from "./BootstrapExample"
import { DateRangePicker } from "react-dates"
import "react-dates/initialize"
import "react-dates/lib/css/_datepicker.css"

//React Date Range Picker
//import "react-date-range/dist/styles.css" // main css file
//import "react-date-range/dist/theme/default.css" // theme css file
import { DateRange } from "react-date-range"
import CustomDateRange from "./CustomDateRange"

function App() {
  const [selectedDate, handleDateChange] = useState(new Date())
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
        <DateRangePicker
          startDate={null} // momentPropTypes.momentObj or null,
          startDateId="11-12-2021" // PropTypes.string.isRequired,
          endDate={null} // momentPropTypes.momentObj or null,
          endDateId="12-12-2021" // PropTypes.string.isRequired,
          onDatesChange={({ startDate, endDate }) => this.setState({ startDate, endDate })} // PropTypes.func.isRequired,
          focusedInput={null} // PropTypes.oneOf([START_DATE, END_DATE]) or null,
          onFocusChange={(focusedInput) => this.setState({ focusedInput })} // PropTypes.func.isRequired,
        />
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
