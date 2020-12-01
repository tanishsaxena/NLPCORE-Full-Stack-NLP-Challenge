import React, { useEffect, useState } from "react";
import axios from "axios";
import WordCloud from "react-d3-cloud";
import { Spinner } from "react-bootstrap";
import "./task2.css";

export const Task2 = () => {
  const [result, updatedata] = useState([]);
  const [loading, updateLoading] = useState(true);
  const fontSizeMapper = (word) => Math.log2(word.value) * 10;
  const fontSizeMapperInitial = (word) => Math.log2(word.value) * 50;
  const rotate = (word) => word.value % 90;

  useEffect(() => {
    document.title = "TASK 2";
    console.log("TASK2");
    axios
      .get("http://127.0.0.1:5000/task2")
      .then((res) => {
        updatedata(res.data);
        updateLoading(false);
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <div>
      {loading ? (
        <div id="Loading">
          <Spinner animation="border" />
        </div>
      ) : (
        <div className="ChartDataFlex">
          {result.map((value, index) => (
            <div className="singleChart">
              <h3>{value["Cluster"]}</h3>
              {index === 0 ? (
                <WordCloud
                  key={index}
                  fontSizeMapper={fontSizeMapperInitial}
                  rotate={rotate}
                  data={value["Data"]}
                />
              ) : (
                <WordCloud
                  key={index}
                  fontSizeMapper={fontSizeMapper}
                  rotate={rotate}
                  data={value["Data"]}
                />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
