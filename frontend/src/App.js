import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { Task1 } from "./container/task1/task1";
import { Main } from "./container/main/main";
import { Task2 } from "./container/task2/task2";
import { Task3 } from "./container/task3/task3";

function App() {
  return (
    <Router>
      <div>
        <Route path="/" exact component={Main} />
        <Route path="/task1" component={Task1} />
        <Route path="/task2" component={Task2} />
        <Route path="/task3" component={Task3} />
      </div>
    </Router>
  );
}

export default App;
