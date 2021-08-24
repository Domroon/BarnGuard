import React from "react"

function Login() {
  return (
    <section class="login-form">
      <div class="container">
        <form class="m-5">
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
          <button type="submit" class="btn btn-primary">
            Senden
          </button>
        </form>
      </div>
    </section>
  )
}

export default Login
