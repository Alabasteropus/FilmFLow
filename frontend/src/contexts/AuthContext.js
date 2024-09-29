// src/contexts/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [authToken, setAuthToken] = useState(() => localStorage.getItem('authToken'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (authToken) {
      // Optionally, decode JWT to get user info
      setUser({ id: 1, username: 'dummy' }); // Replace with actual user data
    }
  }, [authToken]);
 
  const login = async (username, password) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/auth/login', { username, password });
      setAuthToken(response.data.access_token);
      localStorage.setItem('authToken', response.data.access_token);
      setUser({ username });
      return { success: true };
    } catch (error) {
      console.error('Login error:', error.response?.data?.error || error.message);
      return { success: false, message: error.response?.data?.error || 'Login failed.' };
    }
  };

  const register = async (username, password) => {
    try {
      await axios.post('http://127.0.0.1:5000/auth/register', { username, password });
      return { success: true };
    } catch (error) {
      console.error('Registration error:', error.response?.data?.error || error.message);
      return { success: false, message: error.response?.data?.error || 'Registration failed.' };
    }
  };

  const logout = () => {
    setAuthToken(null);
    localStorage.removeItem('authToken');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ authToken, user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
