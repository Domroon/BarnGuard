import React, { useEffect, useState } from "react"
import { Offcanvas, Container, Navbar, Nav, NavDropdown, NavbarBrand, Button } from "react-bootstrap"

function Home() {
  const [show, setShow] = useState(false)
  const handleClose = () => setShow(false)
  const handleShow = () => setShow(true)

  return (
    <div className="App">
      <header className="App-header">
        <Navbar bg="light" expand="xxl">
          <Container>
            <Navbar.Brand href="#home">BarnGuard</Navbar.Brand>
            <Navbar.Toggle onClick={handleShow} />
          </Container>
        </Navbar>

        <Button variant="primary" onClick={handleShow}>
          Launch
        </Button>

        <Offcanvas show={show} onHide={handleClose}>
          <Offcanvas.Header closeButton>
            <Offcanvas.Title>Offcanvas</Offcanvas.Title>
          </Offcanvas.Header>
          <Offcanvas.Body>Some text as placeholder. In real life you can have the elements you have chosen. Like, text, images, lists, etc.</Offcanvas.Body>
        </Offcanvas>
      </header>
    </div>
  )
}

export default Home
