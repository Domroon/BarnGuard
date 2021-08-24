import React, { useState, useEffect } from "react"
import { BrowserRouter, Switch, Route } from "react-router-dom"

import Videos from "./components/Videos"
import Login from "./components/Login"
import Register from "./components/Register"
import ReducedHeader from "./components/ReducedHeader"
import Header from "./components/Header"
import Footer from "./components/Footer"
import StateContext from "./StateContext"

function App() {
  const [loggedIn, setLoggedIn] = useState(false)
  return (
    <>
      <StateContext.Provider value={setLoggedIn}>
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
          </Switch>
          <Footer />
        </BrowserRouter>
      </StateContext.Provider>
    </>
  )
}

export default App
