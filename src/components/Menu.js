import React, { useEffect } from "react"

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
            <a href="#" class="list-group-item list-group-item-action active" aria-current="true">
              {" "}
              Home{" "}
            </a>
            <a href="#" class="list-group-item list-group-item-action">
              Register
            </a>
            <a href="#" class="list-group-item list-group-item-action">
              Login
            </a>
            <a href="#" class="list-group-item list-group-item-action disabled" tabindex="-1" aria-disabled="true">
              A disabled link item
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Menu
