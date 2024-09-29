// src/services/apiService.js
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000'; // Ensure this matches your backend URL

export const generateText = async (prompt) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate-text`, { prompt });
    return response.data.generated_text;
  } catch (error) {
    console.error('Error generating text:', error.response?.data?.error || error.message);
    throw error.response?.data?.error || 'An error occurred while generating text.';
  }
};
