import React, { useState, useRef, useEffect } from "react"
import ReactPlayer from "react-player"
import MaterialIcon from "react-google-material-icons"

function SingleVideo() {
  return (
    <>
      <div className="video-player">
        <div className="row m-2">
          <div className="col">
            <ReactPlayer wrapper="video-player" controls url="http://localhost:5000/uploads/reit.mp4" onReady={() => console.log("onReady callback")} onStart={() => console.log("onStart callback")} />
          </div>
        </div>
      </div>
    </>
  )
}

export default SingleVideo
