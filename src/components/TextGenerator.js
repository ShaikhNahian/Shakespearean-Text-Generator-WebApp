// src/components/TextGenerator.js

import React, { useState } from 'react';

function TextGenerator() {
  const [inputText, setInputText] = useState('');
  const [generatedText, setGeneratedText] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Send the input text to the FastAPI backend for text generation
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ inputText }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setGeneratedText(data.generatedText);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>Shakespearean Text Generator</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Input Text:
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
        </label>
        <button type="submit">Generate</button>
      </form>
      {generatedText && (
        <div>
          <h2>Generated Text:</h2>
          <p>{generatedText}</p>
        </div>
      )}
    </div>
  );
}

export default TextGenerator;
