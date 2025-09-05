const mongoose = require('mongoose');

const activitySchema = new mongoose.Schema({
  timestamp: {
    type: Date,
    default: Date.now,
    required: true
  },
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: false // Not required for system events
  },
  type: {
    type: String,
    required: true,
    enum: [
      'login',
      'logout',
      'profile_update',
      'password_change',
      'admin_action',
      'system_event',
      'security_alert',
      'data_access',
      'configuration_change',
      'biometric_scan'
    ]
  },
  action: {
    type: String,
    required: true
  },
  status: {
    type: String,
    required: true,
    enum: ['success', 'failed', 'suspicious', 'pending', 'blocked']
  },
  details: {
    type: mongoose.Schema.Types.Mixed,
    required: false
  },
  ipAddress: {
    type: String,
    required: false
  },
  userAgent: {
    type: String,
    required: false
  },
  severity: {
    type: String,
    enum: ['low', 'medium', 'high', 'critical'],
    required: true,
    default: 'low'
  },
  relatedEntities: [{
    entityType: String,
    entityId: mongoose.Schema.Types.ObjectId
  }]
});

// Indexes for efficient querying
activitySchema.index({ timestamp: -1 });
activitySchema.index({ user: 1, timestamp: -1 });
activitySchema.index({ type: 1, status: 1 });
activitySchema.index({ severity: 1 });

// Static method to get recent activities
activitySchema.statics.getRecent = async function(limit = 10) {
  return this.find()
    .sort({ timestamp: -1 })
    .limit(limit)
    .populate('user', 'username')
    .exec();
};

// Static method to get user activity history
activitySchema.statics.getUserHistory = async function(userId, limit = 50) {
  return this.find({ user: userId })
    .sort({ timestamp: -1 })
    .limit(limit)
    .exec();
};

// Static method to get security alerts
activitySchema.statics.getSecurityAlerts = async function(hours = 24) {
  const since = new Date(Date.now() - (hours * 3600000));
  return this.find({
    timestamp: { $gte: since },
    $or: [
      { status: 'suspicious' },
      { status: 'blocked' },
      { severity: { $in: ['high', 'critical'] } }
    ]
  })
    .sort({ timestamp: -1 })
    .populate('user', 'username')
    .exec();
};

// Method to format activity for display
activitySchema.methods.formatForDisplay = function() {
  return {
    id: this._id,
    timestamp: this.timestamp.toLocaleString(),
    user: this.user ? this.user.username : 'System',
    type: this.type,
    action: this.action,
    status: this.status,
    severity: this.severity,
    details: this.details
  };
};

const Activity = mongoose.model('Activity', activitySchema);

module.exports = Activity;