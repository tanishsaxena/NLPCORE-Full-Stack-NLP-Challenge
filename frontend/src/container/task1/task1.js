import React, { useEffect, useState } from "react";
import axios from "axios";
import Chart from "react-google-charts";
import { Jumbotron, Spinner, Button } from "react-bootstrap";
import "./task1.css";

export const Task1 = () => {
  const [result, updatedata] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    document.title = "TASK 1";
    axios
      .get("http://127.0.0.1:5000/task1")
      .then((res) => {
        updatedata(res.data);
        setLoading(true);
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <div className="Outer">
      {loading ? (
        <div>
          <Jumbotron id="Heading">
            <h1>TASK 1</h1>
          </Jumbotron>
          <div claaName="ChartBorder1">
            <Chart
              width={1600}
              height={700}
              chartType="ColumnChart"
              loader={<div>Loading Chart</div>}
              data={result["Occur"]}
              options={{
                title: "Top 100 most commonly occured words in documents",
                hAxis: {
                  title: "Words",
                  minValue: 0,
                },
                vAxis: {
                  title: "Occurence",
                },
              }}
              legendToggle
            />
          </div>
          <div className="ChartBorder2">
            <Chart
              width={1600}
              height={700}
              chartType="ColumnChart"
              loader={<div>Loading Chart</div>}
              data={result["Freq"]}
              options={{
                title: "Top 100 most Frequent words in documents",
                colors: ["#b0120a"],
                hAxis: {
                  title: "Words",
                  minValue: 0,
                },
                vAxis: {
                  title: "Frequency",
                },
              }}
              legendToggle
            />
          </div>
        </div>
      ) : (
        <div id="Loading">
          <Spinner animation="border" />
        </div>
      )}
    </div>
  );
};
