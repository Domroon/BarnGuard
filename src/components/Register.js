import React from "react"

function Register() {
  return (
    <section class="register-form">
      <div class="container">
        <h2 className="text-center mt-5">Registrieren</h2>
        <form class="m-5 card p-5">
          <div class="mb-3">
            <label for="name" class="form-label">
              Nickname
            </label>
            <input type="text" class="form-control" id="name" aria-describedby="emailHelp" required></input>
            <div id="emailHelp" class="form-text">
              Wähle einen Nicknamen
            </div>
          </div>
          <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">
              Email-Adresse
            </label>
            <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" required></input>
            <div id="emailHelp" class="form-text">
              Deine Email-Adresse wird nicht weitergegeben.
            </div>
          </div>
          <div class="mb-3">
            <label for="InputPassword1" class="form-label">
              Password
            </label>
            <input type="password" class="form-control" id="InputPassword1" required></input>
          </div>
          <div class="mb-3">
            <label for="InputPassword2" class="form-label">
              Password wiederholen
            </label>
            <input type="password" class="form-control" id="InputPassword2" required></input>
          </div>
          <button type="submit" class="btn btn-primary">
            Senden
          </button>
        </form>
      </div>
    </section>
  )
}

export default Register
