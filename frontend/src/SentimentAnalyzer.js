import React, { useState } from 'react';
import axios from 'axios';

const SentimentAnalyzer = () => {
  const [UserInput, setUserInput] = useState('');
  const [Sentiment, setSentiment] = useState('');
  const [isLoading, setIsLoading] = useState(false); 
  const [errorMsg, setErrorMsg] = useState('');

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
    setErrorMsg(''); // Clear error when typing
  };

  const analyzeSentiment = async () => {
    if (!UserInput.trim()) return; // Don't send empty requests

    setIsLoading(true);
    setSentiment('');
    setErrorMsg('');

    try {
      // 🛑 PASTE YOUR RENDER URL RIGHT HERE 🛑
      const API_URL = 'https://sentiment-analysis-b.onrender.com/predictTweet';
      
      const response = await axios.post(API_URL, {
        text: UserInput,
      });

      // Check if our Python backend sent back an error string
      if (response.data.error) {
        setErrorMsg(response.data.error);
      } else {
        setSentiment(response.data.sentiment);
      }
    } catch (error) {
      console.error("Error: ", error);
      setErrorMsg("Failed to connect to the backend server.");
    } finally {
      setIsLoading(false); // Stop loading animation
    }
  };

  return (
    <div>
      <h2>Twitter Sentiment Analysis</h2>
      <textarea
        rows="4"
        cols="50"
        value={UserInput}
        onChange={handleInputChange}
        placeholder="Enter a tweet"
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

export default SentimentAnalyzer;
