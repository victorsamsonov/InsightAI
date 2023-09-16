import React, { useCallback, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { useDropzone } from "react-dropzone";
import DragDropFiles from "./DragDropFiles";
import "./About.css";
import Recorder from "recorder-js";
import AudioReactRecorder, { RecordState } from "audio-react-recorder";
import axios from "axios";
const MicRecorder = require("mic-recorder-to-mp3");

function About() {
  const [text, setText] = useState("");
  const [isRecording, setIsRecording] = useState(null);
  const [currentRecording, setCurrentRecording] = useState(null);

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
    // Create a FormData object to send the Blob data as a file
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
      })
      .catch((error) => {
        console.error("Failed to upload Blob data to Flask:", error);
        // Handle error
      });
  }

  const onStop = (audioData) => {
    console.log("audioData", audioData);
    setCurrentRecording(audioData);
    downloadAudioBlob(audioData);
    // transcribe();
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

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

  return (
    <div className="dropzone-container">
      <DragDropFiles />
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
        <button className="recording-button" onClick={stopRecording}>
          Stop Recording
        </button>
      ) : (
        <button className="recording-button" onClick={startRecording}>
          Start Recording
        </button>
      )}
      {/* {audioURL && (
        <audio controls>
          <source src={audioURL} type="audio/wav" />
        </audio>
      )} */}

      <AudioReactRecorder
        className="audio-recorder-container"
        state={isRecording}
        onStop={onStop}
        canvasHeight={"50%"}
        backgroundColor={"white"}
        foregroundColor={"#1C82AD"}
      />
    </div>
  );
}

export default About;
