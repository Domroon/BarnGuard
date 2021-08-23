import React, { useEffect } from "react"
import { Button, Row, Col, Form, Container } from "react-bootstrap"

function BootstrapExample() {
  return (
    <Container>
      <Form>
        <Row>
          <Col md>
            <Form.Group controlId="formEmail">
              <Form.Label>Email Address</Form.Label>
              <Form.Control type="email" placeholder="Example@email.com" required></Form.Control>
              <Form.Text className="text-muted" style={{ fontSize: "1rem" }}>
                We'll never share your password!
              </Form.Text>
            </Form.Group>
          </Col>
          <Col md>
            <Form.Group controlId="formPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="password" required></Form.Control>
            </Form.Group>
          </Col>
        </Row>
        <Button variant="secondary" type="submit">
          Login
        </Button>
      </Form>
    </Container>
  )
}

export default BootstrapExample
