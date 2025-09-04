const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const path = require('path');
const systemMonitor = require('./services/SystemMonitor');
const adminRoutes = require('./routes/admin');
const notificationRoutes = require('./routes/notifications');
const securityRoutes = require('./routes/security');
const authRoutes = require('./routes/auth');
const activityLogger = require('./middleware/activityLogger');

const app = express();

// Security middleware
app.use(helmet());
app.use(cors());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Activity logging middleware (disabled for demo mode)
// app.use(activityLogger); // TODO: Enable when MongoDB is configured

// Serve static files from frontend build (DISABLED - Classic HTML Templates Only)
// app.use(express.static(path.join(__dirname, '../frontend/build')));

// Serve static assets for template pages
app.use('/static', express.static(path.join(__dirname, '../static')));
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));
app.use('/css', express.static(path.join(__dirname, '../static/css')));
app.use('/js', express.static(path.join(__dirname, '../static/js')));
app.use('/img', express.static(path.join(__dirname, '../static/img')));

// API Routes
app.use('/api/admin', adminRoutes);
app.use('/api/notifications', notificationRoutes);
app.use('/api/security', securityRoutes);
app.use('/api/auth', authRoutes);

// Root route for API status
app.get('/api', (req, res) => {
  res.json({
    message: 'Biometric Crime Detection API',
    version: '1.0.0',
    status: 'running',
    endpoints: {
      admin: '/api/admin',
      notifications: '/api/notifications',
      security: '/api/security'
    }
  });
});

// Template routes - serve original HTML pages
app.get('/templates/:page', (req, res) => {
  const page = req.params.page;
  const templatePath = path.join(__dirname, '../templates', page);
  
  // Check if file exists and serve it
  if (require('fs').existsSync(templatePath)) {
    res.sendFile(templatePath);
  } else {
    res.status(404).json({ error: 'Template not found' });
  }
});

// Individual template routes for easy access
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/login.html'));
});

app.get('/login-new', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/login_new.html'));
});

app.get('/register', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/register.html'));
});

app.get('/profile', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/profile.html'));
});

app.get('/reports', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/reports.html'));
});

app.get('/match-form', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/match_form.html'));
});

app.get('/match-form-fingerprint', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/match_form_fingerprint.html'));
});

app.get('/match-result', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/match_result.html'));
});

app.get('/view-criminals', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/view_criminals.html'));
});

app.get('/live-face-verification', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/live_face_verification.html'));
});

app.get('/live-fingerprint-verification', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/live_fingerprint_verification.html'));
});

app.get('/fingerprint-match-options', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/fingerprint_match_options.html'));
});

app.get('/admin-management', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/admin_management.html'));
});

app.get('/edit-admin', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/edit_admin.html'));
});

app.get('/cybersecurity-dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/cybersecurity_dashboard.html'));
});

app.get('/admin-dashboard-old', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/admin_dashboard.html'));
});

app.get('/feature-unavailable', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/feature_unavailable.html'));
});

app.get('/original', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/index.html'));
});

app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/dashboard.html'));
});

// Default route - redirect to dashboard (Classic HTML Templates as primary)
app.get('/', (req, res) => {
  res.redirect('/dashboard');
});

// React routes disabled - redirect to classic interface
app.get('/admin/*', (req, res) => {
  res.redirect('/dashboard');
});

// Fallback for unmatched routes
app.get('*', (req, res) => {
  res.redirect('/dashboard');
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ message: 'Something went wrong!' });
});

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost/biometric_crime_detection', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => {
  console.log('Connected to MongoDB');
  // Start system monitoring
  systemMonitor.start();
})
.catch(err => console.error('MongoDB connection error:', err));

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received. Shutting down gracefully...');
  systemMonitor.stop();
  await mongoose.connection.close();
  process.exit(0);
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;