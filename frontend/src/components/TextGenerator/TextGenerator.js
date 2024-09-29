import React, { useState } from 'react';
import { generateText } from '../../services/apiService';
import './TextGenerator.css';

const TextGenerator = () => {
  const [prompt, setPrompt] = useState('');
  const [generatedText, setGeneratedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt.');
      return;
    }

    setLoading(true);
    setError(null);
    setGeneratedText('');

    try {
      const text = await generateText(prompt);
      setGeneratedText(text);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Generate Text with OpenAI</h2>
      <textarea
        className="textarea"
        rows="4"
        placeholder="Enter your prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button className="button" onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>
      {error && <p className="error">{error}</p>}
      {generatedText && (
        <div className="output">
          <h3>Generated Text:</h3>
          <p>{generatedText}</p>
        </div>
      )}
    </div>
  );
};

export default TextGenerator;
