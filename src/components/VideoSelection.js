import { useEffect, useState, useContext } from "react"
import { Link } from "react-router-dom"
import ImageList from "@material-ui/core/ImageList"
import ImageListItem from "@material-ui/core/ImageListItem"
import { ImageListItemBar } from "@material-ui/core"
import { IconButton } from "@material-ui/core"
import MaterialIcon from "react-google-material-icons"
import axios from "axios"
import StateContext from "../StateContext"

function VideoSelection() {
  const [items, setItems] = useState(null)
  const { setVideoname } = useContext(StateContext)

  // useEffect(() => {
  //   // GET request using fetch inside useEffect React hook
  //   axios.get("http://localhost:5000/api/videos").then(function (response) {
  //     // handle success
  //     console.log(response.data)
  //     setItems(response.data)
  //   })
  //   // empty dependency array means this effect will only run once (like componentDidMount in classes)
  // }, [])

  useEffect(() => {
    fetchItems()
  }, [])

  const fetchItems = async () => {
    const data = await fetch("http://localhost:5000/api/videos")

    const items = await data.json()
    setItems(items)
  }

  return (
    <>
      <ImageList rowHeight={200} cols={2}>
        {items
          ? items.map((item) => (
              <ImageListItem key={item.videoname}>
                <img src={`thumbnail/${String(item.thumbnail_photo)}`} alt={item.title} />
                <ImageListItemBar
                  title={item.date}
                  subtitle={<span> {item.time}</span>}
                  actionIcon={
                    <Link to={`/SingleVideo/${item.videoname}`}>
                      <IconButton aria-label={`info about ${item.title}`}>
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#FFFFFF">
                          <path d="M0 0h24v24H0V0z" fill="none" />
                          <path d="M12 6c3.79 0 7.17 2.13 8.82 5.5C19.17 14.87 15.79 17 12 17s-7.17-2.13-8.82-5.5C4.83 8.13 8.21 6 12 6m0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5c1.38 0 2.5 1.12 2.5 2.5S13.38 14 12 14s-2.5-1.12-2.5-2.5S10.62 9 12 9m0-2c-2.48 0-4.5 2.02-4.5 4.5S9.52 16 12 16s4.5-2.02 4.5-4.5S14.48 7 12 7z" />
                        </svg>
                      </IconButton>
                    </Link>
                  }
                />
              </ImageListItem>
            ))
          : " "}
      </ImageList>
    </>
  )
}

export default VideoSelection
