import React, { useContext, useEffect, useState } from "react"
import StateContext from "../StateContext"
import axios from "axios"

function Login() {
  const { setLoggedIn } = useContext(StateContext)
  const [username, setUsername] = useState()
  const [password, setPassword] = useState()
  const { access_token, setAccessToken } = useContext(StateContext)
  const [error, setError] = useState(false)
  const { setRegister_access } = useContext(StateContext)

  useEffect(() => {
    setRegister_access(false)
  })

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      const response = await axios.get(`http://localhost:5000/api/auth/login/${username}/${password}`)
      console.log("User sucessfully logged in.")
      localStorage.setItem("access_token", response.data.access_token)
      setAccessToken(localStorage.getItem("access_token"))
      //console.log(access_token)
      // redirect to videos site!
      setLoggedIn(true)
      setError(false)
    } catch (e) {
      console.log("There was an error.")
      setError(true)
    }
  }

  if (error) {
    return (
      <section class="login">
        <div class="container">
          <div class="alert alert-danger m-5" role="alert">
            Username oder Passwort falsch
          </div>
          <h2 className="text-center mt-5">Login</h2>
          <form onSubmit={handleSubmit} class="mx-5">
            <div className="mb-3">
              <label for="name" className="form-label">
                Nickname
              </label>
              <input onChange={(e) => setUsername(e.target.value)} type="text" className="form-control" id="name" aria-describedby="emailHelp" required></input>
              <div id="emailHelp" className="form-text">
                Bitte gebe Deinen Nicknamen ein
              </div>
            </div>
            <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">
                Passwort
              </label>
              <input onChange={(e) => setPassword(e.target.value)} type="password" class="form-control" id="exampleInputPassword1" required></input>
            </div>
            <button type="submit" class="btn btn-primary">
              Sende
            </button>
          </form>
        </div>
      </section>
    )
  } else {
    return (
      <section class="login">
        <div class="container">
          <h2 className="text-center mt-5">Login</h2>
          <form onSubmit={handleSubmit} class="mx-5">
            <div className="mb-3">
              <label for="name" className="form-label">
                Nickname
              </label>
              <input onChange={(e) => setUsername(e.target.value)} type="text" className="form-control" id="name" aria-describedby="emailHelp" required></input>
              <div id="emailHelp" className="form-text">
                Bitte gebe Deinen Nicknamen ein
              </div>
            </div>
            <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">
                Passwort
              </label>
              <input onChange={(e) => setPassword(e.target.value)} type="password" class="form-control" id="exampleInputPassword1" required></input>
            </div>
            <button type="submit" class="btn btn-primary">
              Sende
            </button>
          </form>
        </div>
      </section>
    )
  }
}

export default Login
