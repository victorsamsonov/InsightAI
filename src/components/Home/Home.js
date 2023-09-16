import React, { useState } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import homeLogo from "../../Assets/home-main.svg";
import Particle from "../Particle";
import Home2 from "./Home2";
import Type from "./Type";
import "./Home.css";
import { Link } from "react-router-dom";
import Nav from "react-bootstrap/Nav";
const handleClick = () => {
  // alert("Button Clicked!");
};
function Home() {
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setSelectedImage(URL.createObjectURL(file));
  };

  return (
    <section>
      <Container fluid className="home-section" id="home">
        {/* <Particle /> */}
        <Container className="home-content">
          <Row>
            <Col md={7} className="home-header">
              <h1 style={{ paddingBottom: 15 }} className="heading">
                Hi There!{" "}
                <span className="wave" role="img" aria-labelledby="wave">
                  👋🏻
                </span>
              </h1>

              <h1 className="heading-name">
                Welcome to
                <strong className="main-name"> InsightAI </strong>
              </h1>

              <div style={{ padding: 50, textAlign: "left" }}>
                <Type />
              </div>
            </Col>
            {/* <Col>
            </Col> */}
            <div className="start-container"></div>
          </Row>
        </Container>
      </Container>
      <button
        style={{ cursor: "pointer" }}
        className="started-button"
        as={Link}
        to="/about"
        // onClick={() => updateExpanded(false)}
      >
        <Nav.Item>
          <Nav.Link as={Link} to="/customize">
            <text style={{ color: "white" }}>Get Started</text>
          </Nav.Link>
        </Nav.Item>
      </button>
    </section>
  );
}

export default Home;
