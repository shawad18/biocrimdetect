const express = require('express');
const router = express.Router();
const Activity = require('../models/Activity');
const { login_required, role_required } = require('../middleware/auth');

// Get security metrics data
router.get('/metrics', [login_required, role_required('admin')], async (req, res) => {
  try {
    // Mock security metrics data for demonstration
    const mockSecurityData = {
      loginAttempts: [
        { timestamp: '00:00', successful: 12, failed: 2 },
        { timestamp: '01:00', successful: 8, failed: 1 },
        { timestamp: '02:00', successful: 5, failed: 0 },
        { timestamp: '03:00', successful: 3, failed: 1 },
        { timestamp: '04:00', successful: 2, failed: 0 },
        { timestamp: '05:00', successful: 4, failed: 0 },
        { timestamp: '06:00', successful: 15, failed: 3 },
        { timestamp: '07:00', successful: 25, failed: 2 },
        { timestamp: '08:00', successful: 35, failed: 4 },
        { timestamp: '09:00', successful: 42, failed: 6 },
        { timestamp: '10:00', successful: 38, failed: 3 },
        { timestamp: '11:00', successful: 41, failed: 5 },
        { timestamp: '12:00', successful: 45, failed: 2 },
        { timestamp: '13:00', successful: 43, failed: 4 },
        { timestamp: '14:00', successful: 39, failed: 7 },
        { timestamp: '15:00', successful: 37, failed: 3 },
        { timestamp: '16:00', successful: 41, failed: 5 },
        { timestamp: '17:00', successful: 44, failed: 6 },
        { timestamp: '18:00', successful: 32, failed: 4 },
        { timestamp: '19:00', successful: 28, failed: 2 },
        { timestamp: '20:00', successful: 22, failed: 3 },
        { timestamp: '21:00', successful: 18, failed: 1 },
        { timestamp: '22:00', successful: 14, failed: 2 },
        { timestamp: '23:00', successful: 10, failed: 1 }
      ],
      threatDistribution: [
        { name: 'Invalid Login', value: 45 },
        { name: 'Failed Biometric', value: 23 },
        { name: 'Unauthorized Access', value: 12 },
        { name: 'Suspicious Activity', value: 8 },
        { name: 'Other', value: 5 }
      ],
      biometricScans: [
        { type: 'Fingerprint', successful: 156, failed: 12, suspicious: 3 },
        { type: 'Face Recognition', successful: 89, failed: 8, suspicious: 2 },
        { type: 'Iris Scan', successful: 45, failed: 3, suspicious: 1 },
        { type: 'Voice Recognition', successful: 23, failed: 5, suspicious: 0 }
      ],
      geographicDistribution: [
        { location: 'New York', authorized: 145, unauthorized: 12 },
        { location: 'Los Angeles', authorized: 98, unauthorized: 8 },
        { location: 'Chicago', authorized: 76, unauthorized: 6 },
        { location: 'Houston', authorized: 54, unauthorized: 4 },
        { location: 'Phoenix', authorized: 43, unauthorized: 3 },
        { location: 'Philadelphia', authorized: 38, unauthorized: 5 },
        { location: 'San Antonio', authorized: 32, unauthorized: 2 },
        { location: 'San Diego', authorized: 28, unauthorized: 3 },
        { location: 'Dallas', authorized: 25, unauthorized: 4 },
        { location: 'San Jose', authorized: 22, unauthorized: 1 }
      ]
    };

    res.json(mockSecurityData);
  } catch (error) {
    console.error('Error fetching security metrics:', error);
    res.status(500).json({ error: 'Failed to fetch security metrics' });
  }
});

// TODO: Replace with real database implementation when MongoDB is configured
/*
router.get('/metrics', [login_required, role_required('admin')], async (req, res) => {
  try {
    const now = new Date();
    const twentyFourHoursAgo = new Date(now - 24 * 60 * 60 * 1000);

    const loginAttempts = await getLoginAttempts(twentyFourHoursAgo, now);
    const threatDistribution = await getThreatDistribution(twentyFourHoursAgo, now);
    const biometricScans = await getBiometricScans(twentyFourHoursAgo, now);
    const geographicDistribution = await getGeographicDistribution(twentyFourHoursAgo, now);

    res.json({
      loginAttempts,
      threatDistribution,
      biometricScans,
      geographicDistribution
    });
  } catch (error) {
    console.error('Error fetching security metrics:', error);
    res.status(500).json({ error: 'Failed to fetch security metrics' });
  }
});
*/

async function getLoginAttempts(startTime, endTime) {
  const hourlyAttempts = await Activity.aggregate([
    {
      $match: {
        type: 'login',
        timestamp: { $gte: startTime, $lte: endTime }
      }
    },
    {
      $group: {
        _id: {
          hour: { $hour: '$timestamp' },
          status: '$status'
        },
        count: { $sum: 1 }
      }
    },
    {
      $group: {
        _id: '$_id.hour',
        attempts: {
          $push: {
            status: '$_id.status',
            count: '$count'
          }
        }
      }
    },
    { $sort: { '_id': 1 } }
  ]);

  return hourlyAttempts.map(hour => ({
    timestamp: `${hour._id}:00`,
    successful: hour.attempts.find(a => a.status === 'success')?.count || 0,
    failed: hour.attempts.find(a => a.status === 'failed')?.count || 0
  }));
}

async function getThreatDistribution(startTime, endTime) {
  const threats = await Activity.aggregate([
    {
      $match: {
        timestamp: { $gte: startTime, $lte: endTime },
        status: { $in: ['failed', 'suspicious'] }
      }
    },
    {
      $group: {
        _id: '$type',
        value: { $sum: 1 }
      }
    }
  ]);

  return threats.map(threat => ({
    name: formatThreatType(threat._id),
    value: threat.value
  }));
}

async function getBiometricScans(startTime, endTime) {
  const scans = await Activity.aggregate([
    {
      $match: {
        type: 'biometric_scan',
        timestamp: { $gte: startTime, $lte: endTime }
      }
    },
    {
      $group: {
        _id: {
          scanType: '$details.scanType',
          status: '$status'
        },
        count: { $sum: 1 }
      }
    }
  ]);

  const scanTypes = [...new Set(scans.map(scan => scan._id.scanType))];

  return scanTypes.map(type => ({
    type,
    successful: scans.find(s => s._id.scanType === type && s._id.status === 'success')?.count || 0,
    failed: scans.find(s => s._id.scanType === type && s._id.status === 'failed')?.count || 0,
    suspicious: scans.find(s => s._id.scanType === type && s._id.status === 'suspicious')?.count || 0
  }));
}

async function getGeographicDistribution(startTime, endTime) {
  const locations = await Activity.aggregate([
    {
      $match: {
        timestamp: { $gte: startTime, $lte: endTime },
        'details.location': { $exists: true }
      }
    },
    {
      $group: {
        _id: {
          location: '$details.location',
          authorized: { $cond: [{ $eq: ['$status', 'success'] }, 'authorized', 'unauthorized'] }
        },
        count: { $sum: 1 }
      }
    },
    {
      $group: {
        _id: '$_id.location',
        access: {
          $push: {
            type: '$_id.authorized',
            count: '$count'
          }
        }
      }
    },
    { $limit: 10 } // Top 10 locations
  ]);

  return locations.map(loc => ({
    location: loc._id,
    authorized: loc.access.find(a => a.type === 'authorized')?.count || 0,
    unauthorized: loc.access.find(a => a.type === 'unauthorized')?.count || 0
  }));
}

function formatThreatType(type) {
  switch (type) {
    case 'login':
      return 'Invalid Login';
    case 'biometric_scan':
      return 'Failed Biometric';
    case 'unauthorized_access':
      return 'Unauthorized Access';
    case 'suspicious_activity':
      return 'Suspicious Activity';
    default:
      return 'Other';
  }
}

module.exports = router;