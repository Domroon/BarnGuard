import React, { useEffect } from "react"
import { NavLink } from "react-router-dom"

function Menu() {
  return (
    <section className="offcanvasSection">
      <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvas" aria-labelledby="offcanvasLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasLabel">
            Offcanvas
          </h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">Content for the offcanvas goes here. You can place just about any Bootstrap component or custom elements here.</div>
      </div>

      <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasExampleLabel">
            Menü
          </h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <div class="list-group">
            <NavLink exact to="/" className="list-group-item list-group-item-action" aria-current="true" activeClassName="active">
              Login
            </NavLink>
            <NavLink to="/registrieren" className="list-group-item list-group-item-action" activeClassName="active">
              Registrieren
            </NavLink>
            <NavLink to="/videos" className="list-group-item list-group-item-action" activeClassName="active">
              Videos
            </NavLink>
            <NavLink to="/profil" className="list-group-item list-group-item-action disabled" tabindex="-1" aria-disabled="true" activeClassName="active">
              Profil
            </NavLink>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Menu
