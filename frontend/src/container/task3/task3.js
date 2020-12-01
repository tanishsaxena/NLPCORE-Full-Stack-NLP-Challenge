import React, { useEffect, useState } from "react";
import axios from "axios";
import Chart from "react-google-charts";
import { Jumbotron, Spinner } from "react-bootstrap";
import "./task3.css";

export const Task3 = () => {
  const [loading, setLoading] = useState(false);

  const [data, updatedata] = useState([]);

  useEffect(() => {
    document.title = "TASK 3";
    console.log("TASK3");
    axios
      .get("http://127.0.0.1:5000/task3")
      .then((res) => {
        updatedata(res.data);
        setLoading(true);
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <div>
      {loading ? (
        <div>
          <Jumbotron id="Heading">
            <h1>TASK 3</h1>
          </Jumbotron>
          <Chart
            width={"1200px"}
            height={"600px"}
            chartType="BubbleChart"
            loader={<div>loading chart!!!</div>}
            data={data["person"]}
            options={{
              title: "Clustering of Documents on the basis of Person Name",
              hAxis: { title: "Attribute 2" },
              vAxis: { title: "Attribute 1" },
              bubble: { textStyle: { fontSize: 0.1 } },
            }}
            rootProps={{ "data-testid": "1" }}
          />

          <Chart
            width={"1200px"}
            height={"600px"}
            chartType="BubbleChart"
            loader={<div>Loading Chart</div>}
            data={data["place"]}
            options={{
              title: "Clustering of Documents on the basis of Place Name",
              hAxis: { title: "Attribute 2" },
              vAxis: { title: "Attribute 1" },
              bubble: { textStyle: { fontSize: 0.1 } },
            }}
            rootProps={{ "data-testid": "1" }}
          />
        </div>
      ) : (
        <div id="Loading">
          <Spinner animation="border" />
        </div>
      )}
    </div>
  );
};
