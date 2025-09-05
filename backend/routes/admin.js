const express = require('express');
const router = express.Router();
const { authenticateAdmin } = require('../middleware/auth');
const SystemStats = require('../models/SystemStats');
const User = require('../models/User');
const Activity = require('../models/Activity');

// Get dashboard data
router.get('/dashboard-data', authenticateAdmin, async (req, res) => {
  try {
    // Mock data for demonstration (replace with real database calls when MongoDB is available)
    const mockData = {
      uptime: '2d 14h 32m 15s',
      activeUsers: 24,
      failedLogins: 7,
      suspiciousActivities: 3,
      recentActivities: [
        {
          timestamp: new Date().toLocaleString(),
          user: 'admin',
          action: 'login',
          status: 'success'
        },
        {
          timestamp: new Date(Date.now() - 300000).toLocaleString(),
          user: 'john_doe',
          action: 'biometric_scan',
          status: 'success'
        },
        {
          timestamp: new Date(Date.now() - 600000).toLocaleString(),
          user: 'unknown',
          action: 'login',
          status: 'failed'
        },
        {
          timestamp: new Date(Date.now() - 900000).toLocaleString(),
          user: 'jane_smith',
          action: 'profile_update',
          status: 'success'
        },
        {
          timestamp: new Date(Date.now() - 1200000).toLocaleString(),
          user: 'system',
          action: 'security_alert',
          status: 'suspicious'
        }
      ]
    };

    res.json(mockData);
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    res.status(500).json({ error: 'Failed to fetch dashboard data' });
  }
});

// TODO: Replace mock data with real database operations when MongoDB is configured
// Example of how to implement with real database:
/*
router.get('/dashboard-data', authenticateAdmin, async (req, res) => {
  try {
    const systemStats = await SystemStats.findOne().sort({ timestamp: -1 });
    const activeUsers = await User.countDocuments({
      lastActivity: { $gte: new Date(Date.now() - 3600000) }
    });
    const failedLogins = await Activity.countDocuments({
      type: 'login',
      status: 'failed',
      timestamp: { $gte: new Date(Date.now() - 86400000) }
    });
    const suspiciousActivities = await Activity.countDocuments({
      status: 'suspicious',
      timestamp: { $gte: new Date(Date.now() - 86400000) }
    });
    const recentActivities = await Activity.find()
      .sort({ timestamp: -1 })
      .limit(10)
      .populate('user', 'username')
      .lean();

    res.json({
      uptime: systemStats ? systemStats.uptime : 'N/A',
      activeUsers,
      failedLogins,
      suspiciousActivities,
      recentActivities: recentActivities.map(activity => ({
        timestamp: activity.timestamp.toLocaleString(),
        user: activity.user ? activity.user.username : 'System',
        action: activity.type,
        status: activity.status
      }))
    });
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    res.status(500).json({ error: 'Failed to fetch dashboard data' });
  }
});
*/

module.exports = router;