import React, { useCallback, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { useDropzone } from "react-dropzone";
import ReactLoading from "react-loading";
import { Link } from "react-router-dom";
import Nav from "react-bootstrap/Nav";
import DragDropFiles from "./DragDropFiles";
import "./About.css";
import Recorder from "recorder-js";
import AudioReactRecorder, { RecordState } from "audio-react-recorder";
import axios from "axios";
import ReactAudioPlayer from "react-audio-player";
import { Robot } from "react-bootstrap-icons";
import "./robot.svg";

// import {  } from 'bootstrap-icons';
const MicRecorder = require("mic-recorder-to-mp3");
const ROBOT = "./robot.svg";
function About() {
  const [text, setText] = useState("");
  const [isRecording, setIsRecording] = useState(null);
  const [isPredict, setIsPredict] = useState(false);
  const [currFiles, setCurrFiles] = useState(null);
  const [isUploaded, setIsUploaded] = useState(false);
  const [currentRecording, setCurrentRecording] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [ocrText, setOcrText] = useState("");
  const [next, setIsNext] = useState(false);
  const [received, setReceived] = useState(false);
  const [audio, setAudio] = useState(null);
  const [audioURL, setAudioURL] = useState(null);
  const [loadChat, setLoadChat] = useState(true);

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

  const obtainLLMResponse = () => {
    // /generate-response
    console.log("LLM");
    axios
      .post("/generate-response", { audio_query: ocrText })
      .then((response) => {
        console.log("LLM");
        console.log(response);
        setAudio(response.data.audio_path);
        setLoadChat(false);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
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
  };

  const predict = () => {
    const formData = new FormData();
    formData.append("audio", currentRecording.blob, "audio.wav");
    formData.append("file", currFiles[0]);
    console.log("predict");
    setProcessing(true);
    setLoadChat(true);
    axios
      .post("/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data", // Make sure to set the content type
        },
      })
      .then((response) => {
        console.log(response);
        setOcrText(response.data.text);
        setIsNext(true);
        setProcessing(false);
        setReceived(true);
      })
      .catch((error) => {
        console.error("Failed to upload Blob data to Flask:", error);
        setProcessing(false);
        // Handle error
      });
    obtainLLMResponse();
  };

  return (
    <div className="about-container">
      <div className="dropzone-container">
        <DragDropFiles
          handleFile={(files, uploaded) => handleFile(files, uploaded)}
        />
        {/* <div className="multi-word-input-container">
          <textarea
            className="multi-word-input"
            placeholder="Enter your prompt"
            value={text}
            onChange={handleTextChange}
          />
        </div> */}
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
              Get Answer
            </button>
          </>
        )}
        {/* {audioURL && (
          <audio controls>
            <source src={audioURL} type="audio/wav" />
          </audio>
        )} */}
        {processing === true ? (
          <div className="audio-recorder-container">
            <ReactLoading type="bars" color="#a317a3" className="loader" />
          </div>
        ) : (
          <div className="no-loader"></div>
        )}
        <div className="audio-recorder-container">
          <AudioReactRecorder
            state={isRecording}
            onStop={onStop}
            canvasHeight={"50%"}
            backgroundColor={"white"}
            foregroundColor={"#1C82AD"}
          />
        </div>

        {/* <ReactLoading type="bars" color="red"/> */}
      </div>
      <div className="chat-container">
        <h1 style={{ color: "white" }}>Chat</h1>
        <div className="chat-box">
          {received ? (
            <div className={"audio-wrapper"}>
              <img className="avatar" src={require("./avatar.png")} />
              { loadChat ?
                <ReactLoading
                  type="bubbles"
                  color="#17a34a"
                  className="loader"
                /> : <div style={{"minHeight":"30px"}}></div>
              }
              <ReactAudioPlayer
                src={`data:audio/wav;base64,${audio}`}
                controls={true}
              />
            </div>
          ) : (
            <h1 className="filler">Upload an image and question</h1>
          )}
        </div>
      </div>
    </div>
  );
}

export default About;
