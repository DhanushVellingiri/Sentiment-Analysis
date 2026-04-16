import React, { useState } from 'react';
import axios from 'axios';

const YTSentimentAnalyzer = () => {
  const [UserInput, setUserInput] = useState('');
  const [Sentiment, setSentiment] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
    setErrorMsg('');
  };

  const analyzeSentiment = async () => {
    if (!UserInput.trim()) return;

    setIsLoading(true);
    setSentiment('');
    setErrorMsg('');

    try {
      const API_URL = 'https://sentiment-analysis-b.onrender.com/predictYT';
      
      const response = await axios.post(API_URL, {
        comment: UserInput, // Backend expects 'comment'
      });

      if (response.data.error) {
        setErrorMsg(response.data.error);
      } else {
        setSentiment(response.data.sentiment);
      }
    } catch (error) {
      console.error("Error: ", error);
      setErrorMsg("Failed to connect to the backend server.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h2>YouTube Comment Sentiment Analysis</h2>
      <textarea
        rows="4"
        cols="50"
        value={UserInput}
        onChange={handleInputChange}
        placeholder="Enter a YouTube comment"
      ></textarea>
      <br />
      <button onClick={analyzeSentiment} disabled={isLoading}>
        {isLoading ? 'Analyzing...' : 'Analyze Sentiment'}
      </button>
      
      {Sentiment && <p><strong>Predicted Sentiment:</strong> {Sentiment}</p>}
      {errorMsg && <p style={{ color: 'red' }}>{errorMsg}</p>}
    </div>
  );
};

export default YTSentimentAnalyzer;
