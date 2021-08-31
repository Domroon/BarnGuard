import React, { useState } from "react"
import axios from "axios"

function Register() {
  const [error, setError] = useState(false)
  const [username, setUsername] = useState()
  const [email, setEmail] = useState()
  const [password, setPassword] = useState()
  const [passwordRepetition, setPasswordRepetition] = useState()

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      await axios.post("http://localhost:5000/api/user", { username, email, password })
      console.log("User sucessfully created.")
    } catch (e) {
      console.log("There was an error.")
    }
  }

  return (
    <section className="register-form">
      <div className="container">
        <h2 className="text-center mt-5">Registrieren</h2>
        <form onSubmit={handleSubmit} className="m-5 card p-5">
          <div className="mb-3">
            <label for="name" className="form-label">
              Nickname
            </label>
            <input onChange={(e) => setUsername(e.target.value)} type="text" className="form-control" id="name" aria-describedby="emailHelp" required></input>
            <div id="emailHelp" className="form-text">
              Wähle einen Nicknamen
            </div>
          </div>
          <div className="mb-3">
            <label for="exampleInputEmail1" className="form-label">
              Email-Adresse
            </label>
            <input onChange={(e) => setEmail(e.target.value)} type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" required></input>
            <div id="emailHelp" className="form-text">
              Deine Email-Adresse wird nicht weitergegeben.
            </div>
          </div>
          <div className="mb-3">
            <label for="InputPassword1" className="form-label">
              Password
            </label>
            <input onChange={(e) => setPassword(e.target.value)} type="password" className="form-control" id="InputPassword1" required></input>
          </div>
          <div className="mb-3">
            <label for="InputPassword2" className="form-label">
              Password wiederholen
            </label>
            <input onChange={(e) => setPasswordRepetition(e.target.value)} type="password" className="form-control" id="InputPassword2" required></input>
          </div>
          <button className="btn btn-primary">Senden</button>
        </form>
      </div>
    </section>
  )
}

export default Register
