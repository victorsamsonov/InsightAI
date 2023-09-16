import React from "react";
import Typewriter from "typewriter-effect";
import "./Type.css";

function Type() {
  return (
    <Typewriter
      className="typewriter"
      options={{
        strings: [
          "Chase your learning goals and curiosity",
          "Interact with students from your institution",
          "Use AI to obtain improved answers",
        ],
        autoStart: true,
        loop: true,
        deleteSpeed: 50,
      }}
      style={{ border: "1px solid red" }}
    />
  );
}

export default Type;
