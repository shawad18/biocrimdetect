const Activity = require('../models/Activity');

const activityLogger = async (req, res, next) => {
  const originalSend = res.send;
  const startTime = Date.now();

  // Get user IP and user agent
  const ipAddress = req.ip || req.connection.remoteAddress;
  const userAgent = req.headers['user-agent'];

  // Determine activity type based on request path
  const getActivityType = (path) => {
    if (path.includes('/auth')) return 'login';
    if (path.includes('/admin')) return 'admin_action';
    if (path.includes('/biometric')) return 'biometric_scan';
    if (path.includes('/profile')) return 'profile_update';
    return 'system_event';
  };

  // Determine severity based on method and path
  const getSeverity = (method, path) => {
    if (method === 'DELETE' || path.includes('/admin')) return 'high';
    if (method === 'PUT' || method === 'POST') return 'medium';
    return 'low';
  };

  try {
    // Override response send method to capture status
    res.send = function (data) {
      const endTime = Date.now();
      const responseTime = endTime - startTime;

      // Create activity log
      const activity = {
        timestamp: new Date(),
        user: req.user ? req.user._id : null,
        type: getActivityType(req.path),
        action: `${req.method} ${req.path}`,
        status: res.statusCode >= 400 ? 'failed' : 'success',
        details: {
          method: req.method,
          path: req.path,
          query: req.query,
          responseTime,
          statusCode: res.statusCode
        },
        ipAddress,
        userAgent,
        severity: getSeverity(req.method, req.path)
      };

      // Add request body for non-GET requests, excluding sensitive data
      if (req.method !== 'GET') {
        const sanitizedBody = { ...req.body };
        delete sanitizedBody.password;
        delete sanitizedBody.token;
        activity.details.body = sanitizedBody;
      }

      // Log suspicious activities
      if (res.statusCode === 401 || res.statusCode === 403) {
        activity.status = 'suspicious';
        activity.severity = 'high';
      }

      // Async log creation - don't wait for it
      Activity.create(activity).catch(err => {
        console.error('Error creating activity log:', err);
      });

      // Call original send
      originalSend.call(this, data);
    };

    next();
  } catch (error) {
    console.error('Error in activity logger:', error);
    next(error);
  }
};

module.exports = activityLogger;