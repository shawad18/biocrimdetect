const express = require('express');
const router = express.Router();
const path = require('path');

// Mock user database (replace with real database in production)
const users = [
  { id: 1, username: 'admin', password: 'admin123', role: 'admin' },
  { id: 2, username: 'user', password: 'user123', role: 'user' },
  { id: 3, username: 'demo', password: 'demo', role: 'user' },
  { id: 4, username: 'shawad', password: 'password123', role: 'admin' }
];

// Login endpoint
router.post('/login', (req, res) => {
  const { username, password } = req.body;
  
  // Find user
  const user = users.find(u => u.username === username && u.password === password);
  
  if (user) {
    // Successful login - redirect to dashboard
    res.json({
      success: true,
      message: 'Login successful',
      user: {
        id: user.id,
        username: user.username,
        role: user.role
      },
      redirectUrl: '/dashboard'
    });
  } else {
    // Failed login
    res.status(401).json({
      success: false,
      message: 'Invalid username or password'
    });
  }
});

// Register endpoint (basic implementation)
router.post('/register', (req, res) => {
  const { username, password, email } = req.body;
  
  // Check if user already exists
  const existingUser = users.find(u => u.username === username);
  
  if (existingUser) {
    return res.status(400).json({
      success: false,
      message: 'Username already exists'
    });
  }
  
  // Create new user
  const newUser = {
    id: users.length + 1,
    username,
    password, // In production, hash this password
    role: 'user'
  };
  
  users.push(newUser);
  
  res.json({
    success: true,
    message: 'Registration successful',
    user: {
      id: newUser.id,
      username: newUser.username,
      role: newUser.role
    },
    redirectUrl: '/original'
  });
});

// Logout endpoint
router.post('/logout', (req, res) => {
  res.json({
    success: true,
    message: 'Logout successful',
    redirectUrl: '/login'
  });
});

module.exports = router;