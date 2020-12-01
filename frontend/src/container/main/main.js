import React from "react";
import { Link } from "react-router-dom";
import { Button, Jumbotron } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "./main.css";

export const Main = () => {
  document.title = "NLPCORE";
  return (
    <div>
      <Jumbotron id="Heading">
        <h1>NLPCORE Hiring Competition</h1>
      </Jumbotron>
      <div id="Link1">
        <Link to="/task1">
          <Button size="lg" variant="primary">
            Task1
          </Button>{" "}
        </Link>
      </div>
      <div id="Link2">
        <Link to="/task2">
          <Button size="lg" variant="primary">
            Task2
          </Button>{" "}
        </Link>
      </div>
      <div id="Link3">
        <Link to="/task3">
          <Button size="lg" variant="primary">
            Task3
          </Button>{" "}
        </Link>
      </div>
      <Jumbotron id="Footer">
        <h1>Submitted By Tanish Saxena</h1>
      </Jumbotron>
    </div>
  );
};
