import React, { useCallback, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { useDropzone } from "react-dropzone";
import ReactLoading from "react-loading";

import DragDropFiles from "./DragDropFiles";
import "./About.css";
import Recorder from "recorder-js";
import AudioReactRecorder, { RecordState } from "audio-react-recorder";
import axios from "axios";
const MicRecorder = require("mic-recorder-to-mp3");

function About() {
  const [text, setText] = useState("");
  const [isRecording, setIsRecording] = useState(null);
  const [isPredict, setIsPredict] = useState(false);
  const [currFiles, setCurrFiles] = useState(null);
  const [isUploaded, setIsUploaded] = useState(false);
  const [currentRecording, setCurrentRecording] = useState(null);
  const [processing, setProcessing] = useState(false);

  const [audioURL, setAudioURL] = useState(null);

  function transcribe() {
    console.log("axios");
    axios
      .post("/transcribe")
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }
  const recorder = new MicRecorder({
    bitRate: 128,
  });
  const onDrop = useCallback((acceptedFiles) => {
    // Do something with the uploaded file, e.g., send it to a server
    console.log(acceptedFiles);
  }, []);

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  function downloadAudioBlob(audioBlob) {
    const blobData = audioBlob;
    setProcessing(true);
    const formData = new FormData();
    formData.append("audio", blobData.blob, "audio.wav");
    // Send the Blob data to your Flask backend using Axios
    axios
      .post("/save-recording", formData, {
        headers: {
          "Content-Type": "multipart/form-data", // Make sure to set the content type
        },
      })
      .then((response) => {
        console.log(response);
        setProcessing(false);
      })
      .catch((error) => {
        console.error("Failed to upload Blob data to Flask:", error);
        setProcessing(false);
        // Handle error
      });
  }

  const onStop = (audioData) => {
    console.log("audioData", audioData);
    setCurrentRecording(audioData);
    downloadAudioBlob(audioData);
    let pred = audioData !== null && currFiles !== null ? true : false;
    console.log(audioData);
    console.log(currFiles);
    console.log("pred");
    console.log(pred);
    setIsPredict(pred);
    // transcribe();
  };

  const startRecording = async () => {
    try {
      setIsRecording(RecordState.START);
    } catch (error) {
      console.error("Failed to start recording:", error);
    }
  };

  const stopRecording = async () => {
    try {
      setIsRecording(RecordState.STOP);
    } catch (error) {
      console.error("Failed to stop recording:", error);
    }
  };

  const handleFile = (files, uploaded) => {
    setCurrFiles(files);
    setIsUploaded(uploaded);
    let pred = currentRecording !== null && files !== null ? true : false;
    console.log("pred");
    console.log(pred);
    setIsPredict(pred);
    // console.log("files");
    // console.log(files);
    // console.log("uploaded")
    // console.log(uploaded);
  };

  const predict = () => {
    const formData = new FormData();
    formData.append("audio", currentRecording.blob, "audio.wav");
    formData.append("file", currFiles[0]);
    console.log("predict");
    setProcessing(true);
    axios
      .post("/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data", // Make sure to set the content type
        },
      })
      .then((response) => {
        console.log(response);
        setProcessing(false);
      })
      .catch((error) => {
        console.error("Failed to upload Blob data to Flask:", error);
        setProcessing(false);
        // Handle error
      });
  };

  return (
    <div className="dropzone-container">
      <DragDropFiles
        handleFile={(files, uploaded) => handleFile(files, uploaded)}
      />
      <div className="multi-word-input-container">
        <textarea
          className="multi-word-input"
          placeholder="Enter your prompt"
          value={text}
          onChange={handleTextChange}
        />
      </div>
      <h1 className="record-title">Audio Recorder</h1>
      {isRecording == RecordState.START ? (
        <>
          <button className="recording-button" onClick={stopRecording}>
            Stop Recording
          </button>
          <button className="predict-button" disabled={!isPredict}>
            Predict
          </button>
        </>
      ) : (
        <>
          <button className="recording-button" onClick={startRecording}>
            Start Recording
          </button>
          <button
            className="predict-button"
            disabled={!isPredict}
            onClick={predict}
          >
            Predict
          </button>
        </>
      )}
      {/* {audioURL && (
        <audio controls>
          <source src={audioURL} type="audio/wav" />
        </audio>
      )} */}
      {processing === true ? (
        <ReactLoading type="bars" color="#a317a3" className="loader" />
      ) : (
        <div className="loader"></div>
      )}
      <AudioReactRecorder
        className="audio-recorder-container"
        state={isRecording}
        onStop={onStop}
        canvasHeight={"50%"}
        backgroundColor={"white"}
        foregroundColor={"#1C82AD"}
      />
      {/* <ReactLoading type="bars" color="red"/> */}
    </div>
  );
}

export default About;
