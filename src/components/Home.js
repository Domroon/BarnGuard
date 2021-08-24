import React from "react"
import Footer from "./Footer"
import Header from "./Header"

function Home() {
  return (
    <div className="App">
      <Header />
      <section class="movie-cards">
        <div class="container">
          <div id="app" class="row justify-content-sm-center"></div>
        </div>
      </section>
      <Footer />
    </div>
  )
}

export default Home
