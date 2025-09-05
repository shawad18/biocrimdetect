// Simple auth middleware for demo purposes
// In production, use proper JWT authentication

const login_required = (req, res, next) => {
  // For demo purposes, we'll simulate an authenticated user
  // In production, verify JWT token here
  req.user = {
    _id: 'demo_user_id',
    username: 'demo_user',
    role: 'admin'
  };
  next();
};

const role_required = (role) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }
    
    if (req.user.role !== role) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    
    next();
  };
};

const authenticateAdmin = (req, res, next) => {
  // For demo purposes, we'll simulate an admin user
  req.user = {
    _id: 'admin_user_id',
    username: 'admin',
    role: 'admin'
  };
  next();
};

module.exports = {
  login_required,
  role_required,
  authenticateAdmin
};