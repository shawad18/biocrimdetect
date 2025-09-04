const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true
  },
  role: {
    type: String,
    enum: ['user', 'admin', 'moderator'],
    default: 'user'
  },
  profile: {
    firstName: String,
    lastName: String,
    dateOfBirth: Date,
    phoneNumber: String,
    address: {
      street: String,
      city: String,
      state: String,
      zipCode: String,
      country: String
    }
  },
  biometricData: {
    faceEncoding: [Number],
    fingerprintHash: String,
    voicePrint: String
  },
  securitySettings: {
    twoFactorEnabled: {
      type: Boolean,
      default: false
    },
    loginNotifications: {
      type: Boolean,
      default: true
    },
    sessionTimeout: {
      type: Number,
      default: 3600 // 1 hour in seconds
    }
  },
  lastActivity: {
    type: Date,
    default: Date.now
  },
  loginHistory: [{
    timestamp: {
      type: Date,
      default: Date.now
    },
    ipAddress: String,
    userAgent: String,
    success: Boolean
  }],
  isActive: {
    type: Boolean,
    default: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

// Indexes for efficient querying
userSchema.index({ username: 1 });
userSchema.index({ email: 1 });
userSchema.index({ lastActivity: -1 });
userSchema.index({ role: 1 });

// Update the updatedAt field before saving
userSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});

// Method to update last activity
userSchema.methods.updateLastActivity = function() {
  this.lastActivity = new Date();
  return this.save();
};

// Static method to get active users
userSchema.statics.getActiveUsers = async function(timeframe = 3600000) { // 1 hour default
  const since = new Date(Date.now() - timeframe);
  return this.countDocuments({
    lastActivity: { $gte: since },
    isActive: true
  });
};

// Method to add login attempt to history
userSchema.methods.addLoginAttempt = function(ipAddress, userAgent, success) {
  this.loginHistory.push({
    timestamp: new Date(),
    ipAddress,
    userAgent,
    success
  });
  
  // Keep only last 50 login attempts
  if (this.loginHistory.length > 50) {
    this.loginHistory = this.loginHistory.slice(-50);
  }
  
  return this.save();
};

const User = mongoose.model('User', userSchema);

module.exports = User;