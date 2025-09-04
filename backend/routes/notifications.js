const express = require('express');
const router = express.Router();
const Activity = require('../models/Activity');
const { login_required } = require('../middleware/auth');

// Get all notifications for the current user
router.get('/', login_required, async (req, res) => {
  try {
    // Mock notifications data for demonstration
    const mockNotifications = [
      {
        id: '1',
        type: 'security',
        title: 'Security Alert',
        message: 'Suspicious login attempt detected from unknown IP address',
        severity: 'high',
        timestamp: new Date(),
        read: false
      },
      {
        id: '2',
        type: 'error',
        title: 'Login Failed',
        message: 'Failed login attempt from 192.168.1.100 - Invalid credentials',
        severity: 'medium',
        timestamp: new Date(Date.now() - 300000),
        read: false
      },
      {
        id: '3',
        type: 'info',
        title: 'System Update',
        message: 'System monitoring service started successfully',
        severity: 'low',
        timestamp: new Date(Date.now() - 600000),
        read: true
      },
      {
        id: '4',
        type: 'warning',
        title: 'Biometric Scan',
        message: 'Suspicious biometric scan detected: Fingerprint mismatch',
        severity: 'medium',
        timestamp: new Date(Date.now() - 900000),
        read: false
      },
      {
        id: '5',
        type: 'info',
        title: 'Admin Action',
        message: 'Administrative action: User permissions updated',
        severity: 'low',
        timestamp: new Date(Date.now() - 1200000),
        read: true
      }
    ];

    res.json(mockNotifications);
  } catch (error) {
    console.error('Error fetching notifications:', error);
    res.status(500).json({ error: 'Failed to fetch notifications' });
  }
});

// TODO: Replace with real database implementation when MongoDB is configured
/*
router.get('/', login_required, async (req, res) => {
  try {
    const userId = req.user._id;
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 50;

    const activities = await Activity.find({
      $or: [
        { severity: 'high' },
        { type: 'login', status: 'failed' },
        { status: 'suspicious' },
        { type: 'admin_action' },
        { user: userId }
      ]
    })
      .sort({ timestamp: -1 })
      .skip((page - 1) * limit)
      .limit(limit)
      .lean();

    const notifications = activities.map(activity => ({
      id: activity._id,
      type: getNotificationType(activity),
      title: getNotificationTitle(activity),
      message: getNotificationMessage(activity),
      severity: activity.severity,
      timestamp: activity.timestamp,
      read: activity.read || false
    }));

    res.json(notifications);
  } catch (error) {
    console.error('Error fetching notifications:', error);
    res.status(500).json({ error: 'Failed to fetch notifications' });
  }
});
*/

// Mark a notification as read
router.put('/:id/read', login_required, async (req, res) => {
  try {
    const notificationId = req.params.id;
    
    // Mock implementation - in real app, this would update the database
    console.log(`Marking notification ${notificationId} as read for user ${req.user._id}`);
    
    // Simulate successful update
    res.json({ 
      success: true, 
      message: 'Notification marked as read',
      notificationId: notificationId,
      readAt: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error marking notification as read:', error);
    res.status(500).json({ error: 'Failed to mark notification as read' });
  }
});

// TODO: Replace with real database implementation when MongoDB is configured
/*
router.put('/:id/read', login_required, async (req, res) => {
  try {
    const activityId = req.params.id;
    
    await Activity.findByIdAndUpdate(activityId, {
      read: true,
      readAt: new Date(),
      readBy: req.user._id
    });

    res.json({ success: true });
  } catch (error) {
    console.error('Error marking notification as read:', error);
    res.status(500).json({ error: 'Failed to mark notification as read' });
  }
});
*/

// Helper functions to format notifications
function getNotificationType(activity) {
  if (activity.severity === 'high') return 'security';
  if (activity.status === 'failed') return 'error';
  if (activity.status === 'suspicious') return 'warning';
  return 'info';
}

function getNotificationTitle(activity) {
  switch (activity.type) {
    case 'login':
      return activity.status === 'failed' ? 'Login Failed' : 'Login Success';
    case 'admin_action':
      return 'Admin Action';
    case 'biometric_scan':
      return 'Biometric Scan';
    case 'profile_update':
      return 'Profile Updated';
    default:
      return 'System Event';
  }
}

function getNotificationMessage(activity) {
  let message = '';

  switch (activity.type) {
    case 'login':
      message = `Login attempt from ${activity.ipAddress}`;
      if (activity.status === 'failed') {
        message += ' - Invalid credentials';
      }
      break;

    case 'admin_action':
      message = `Administrative action: ${activity.action}`;
      break;

    case 'biometric_scan':
      message = `Biometric scan ${activity.status}: ${activity.details?.scanType || 'Unknown type'}`;
      break;

    case 'profile_update':
      message = 'User profile information was updated';
      break;

    default:
      message = activity.action;
  }

  return message;
}

module.exports = router;