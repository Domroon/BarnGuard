import React, { useContext } from "react"
import StateContext from "../StateContext"

function Login() {
  const context = useContext(StateContext)
  return (
    <section class="login">
      <div class="container">
        <h2 className="text-center mt-5">Login</h2>
        <form class="mx-5">
          <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">
              Email Adresse
            </label>
            <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" required></input>
            <div id="emailHelp" class="form-text">
              Wir teilen Deine E-Mail Adresse mit niemandem.
            </div>
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">
              Passwort
            </label>
            <input type="password" class="form-control" id="exampleInputPassword1" required></input>
          </div>
          <button onClick={context} type="submit" class="btn btn-primary">
            Senden
          </button>
        </form>
      </div>
    </section>
  )
}

export default Login
