import React, { useEffect, useState } from "react"
import Header from "./Header"

function Home() {
  const [show, setShow] = useState(false)
  const handleClose = () => setShow(false)
  const handleShow = () => setShow(true)

  return (
    <div className="App">
      <Header />
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

      <section class="movie-cards">
        <div class="container">
          <div id="app" class="row justify-content-sm-center"></div>
        </div>
      </section>

      <footer>
        <div class="container py-3 my-4">
          <ul class="nav justify-content-center border-bottom pb-3 mb-3">
            <li class="nav-item">
              <a href="#" class="nav-link px-2 text-muted">
                Home
              </a>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link px-2 text-muted">
                Features
              </a>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link px-2 text-muted">
                Pricing
              </a>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link px-2 text-muted">
                FAQs
              </a>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link px-2 text-muted">
                About
              </a>
            </li>
          </ul>
          <p class="text-center text-muted">&copy; 2021 BarnGuard</p>
        </div>
      </footer>
    </div>
  )
}

export default Home
