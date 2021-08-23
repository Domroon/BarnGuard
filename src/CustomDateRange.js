import "react-date-range/dist/styles.css" // main css file
import "react-date-range/dist/theme/default.css" // theme css file

import { DateRangePicker } from "react-date-range"

class CustomDateRange extends DateRangePicker {
  handleSelect(ranges) {
    console.log(ranges)
    // {
    //   selection: {
    //     startDate: [native Date Object],
    //     endDate: [native Date Object],
    //   }
    // }
  }
  render() {
    const selectionRange = {
      startDate: new Date(),
      endDate: new Date(),
      key: "selection",
    }
    return <DateRangePicker ranges={[selectionRange]} onChange={this.handleSelect} />
  }
}

export default CustomDateRange
