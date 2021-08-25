import React, { useState } from "react"
import ReactPlayer from "react-player"

function SingleVideo() {
  // Render a YouTube video player

  return (
    <>
      <ReactPlayer playing={true} url="http://localhost:5000/uploads/reit.mp4" />
    </>
  )
}

export default SingleVideo
