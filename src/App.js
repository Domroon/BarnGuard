import React, { useState } from "react"
import { BrowserRouter, Switch, Route } from "react-router-dom"

import Videos from "./components/Videos"
import Login from "./components/Login"
import Register from "./components/Register"
import ReducedHeader from "./components/ReducedHeader"
import Header from "./components/Header"
import Footer from "./components/Footer"
import StateContext from "./StateContext"
import SingleVideo from "./components/SingleVideo"

function App() {
  const [loggedIn, setLoggedIn] = useState(false)
  const [videoname, setVideoname] = useState(null)

  return (
    <>
      <StateContext.Provider value={{ setLoggedIn, setVideoname, videoname }}>
        <BrowserRouter>
          {loggedIn ? <Header /> : <ReducedHeader />}
          <Switch>
            <Route path="/videos">
              <Videos />
            </Route>
            <Route path="/login">
              <Login />
            </Route>
            <Route path="/registrieren">
              <Register />
            </Route>
            <Route path="/singleVideo">
              <div className="row m-2">
                <div className="col d-flex justify-content-center">
                  <SingleVideo />
                </div>
              </div>
            </Route>
          </Switch>
          <Footer />
        </BrowserRouter>
      </StateContext.Provider>
    </>
  )
}

export default App
