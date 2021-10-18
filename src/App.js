import React, { useState } from "react"
import { BrowserRouter, Switch, Route, Redirect } from "react-router-dom"

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
  const [access_token, setAccessToken] = useState(localStorage.getItem("access_token"))
  const [register_access, setRegister_access] = useState()

  return (
    <>
      <StateContext.Provider value={{ setLoggedIn, setVideoname, videoname, access_token, setAccessToken, setRegister_access, register_access }}>
        <BrowserRouter>
          {loggedIn ? <Header /> : <ReducedHeader />}
          <Switch>
            <Route exact path="/videos">
              <Videos />
            </Route>
            <Route exact path="/">
              {loggedIn ? <Redirect to="/videos" /> : <Login />}
            </Route>
            <Route path="/registrieren">{register_access ? <Redirect to="/" /> : <Register />}</Route>
            <Route path="/singleVideo/:videoname" component={SingleVideo} />
          </Switch>
          <Footer />
        </BrowserRouter>
      </StateContext.Provider>
    </>
  )
}

export default App
