import React, { useState } from "react"
import "react-dates/initialize"
import "react-dates/lib/css/_datepicker.css"
import { DateRangePicker, SingleDatePicker, DayPickerRangeController } from "react-dates"

function Videos() {
  const [dateRange, setdateRange] = useState({
    startDate: null,
    endDate: null,
  })
  const [focus, setFocus] = useState(null)

  const { startDate, endDate } = dateRange

  const handleOnDateChange = (startDate, endDate) => setdateRange(startDate, endDate)
  return (
    <div className="App">
      <section class="videos">
        <div class="container text-center">
          <h2 className="text-center mt-5">Videos</h2>
          <div className="row m-2">
            <div className="col">
              <DateRangePicker withPortal autoFocus displayFormat="DD.MM.YYYY" isOutsideRange={() => false} keepOpenOnDateSelect={true} startDatePlaceholderText="Startdatum" startDate={startDate} onDatesChange={handleOnDateChange} endDatePlaceholderText="Enddatum" endDate={endDate} numberOfMonths={1} showClearDates={true} focusedInput={focus} onFocusChange={(focus) => setFocus(focus)} startDateId="startDateMookh" endDateId="endDateMookh" minimumNights={0} />
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Videos
