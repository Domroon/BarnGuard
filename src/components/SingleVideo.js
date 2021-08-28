import React, { useState, useRef, useEffect, useContext } from "react"
import ReactPlayer from "react-player"
import MaterialIcon from "react-google-material-icons"
import StateContext from "../StateContext"

function SingleVideo(props) {
  const { videoname } = useContext(StateContext)

  return (
    <>
      <div className="video-player">
        <div className="row m-2">
          <div className="col">
            <ReactPlayer wrapper="video-player" controls url={`http://localhost:5000/videos/${videoname}`} onReady={() => console.log("onReady callback")} onStart={() => console.log("onStart callback")} />
          </div>
        </div>
      </div>
    </>
  )
}

export default SingleVideo
