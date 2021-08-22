import React, { useEffect } from "react"
import { Button, Card } from "react-bootstrap"

function CardExample() {
  return (
    <Card className="m-5">
      <Card.Img src="https://picsum.photos/200/100" />
      <Card.Body>
        <Card.Title style={{ color: "black" }}>Card Example</Card.Title>
        <Card.Text style={{ color: "black", fontSize: "1rem" }}>This is an example of react bootstrap cards.</Card.Text>
        <Button variant="danger">Read More</Button>
      </Card.Body>
    </Card>
  )
}

export default CardExample
