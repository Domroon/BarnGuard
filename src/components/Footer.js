import React from "react"
import { Link } from "react-router-dom"

function Footer() {
  return (
    <footer>
      <div class="container py-3 my-4">
        <ul class="nav justify-content-center border-bottom pb-3 mb-3">
          <li class="nav-item">
            <Link to="/registrieren" class="nav-link px-2 text-muted">
              Registrieren
            </Link>
          </li>
        </ul>
        <p class="text-center text-muted">&copy; 2021 BarnGuard</p>
      </div>
    </footer>
  )
}

export default Footer
