const mongoose = require('mongoose');

const systemStatsSchema = new mongoose.Schema({
  timestamp: {
    type: Date,
    default: Date.now,
    required: true
  },
  uptime: {
    type: String,
    required: true
  },
  cpuUsage: {
    type: Number,
    required: true,
    min: 0,
    max: 100
  },
  memoryUsage: {
    total: Number,
    used: Number,
    free: Number,
    percentUsed: Number
  },
  diskUsage: {
    total: Number,
    used: Number,
    free: Number,
    percentUsed: Number
  },
  networkStats: {
    bytesReceived: Number,
    bytesSent: Number,
    packetsReceived: Number,
    packetsSent: Number
  },
  activeConnections: {
    type: Number,
    default: 0
  },
  lastUpdate: {
    type: Date,
    default: Date.now
  }
});

// Index for efficient querying of recent stats
systemStatsSchema.index({ timestamp: -1 });

// Method to format uptime
systemStatsSchema.methods.formatUptime = function() {
  const seconds = Math.floor(process.uptime());
  const days = Math.floor(seconds / (3600 * 24));
  const hours = Math.floor((seconds % (3600 * 24)) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;

  return `${days}d ${hours}h ${minutes}m ${remainingSeconds}s`;
};

// Static method to get latest stats
systemStatsSchema.statics.getLatest = async function() {
  return this.findOne().sort({ timestamp: -1 }).exec();
};

// Static method to get stats history
systemStatsSchema.statics.getHistory = async function(hours = 24) {
  const since = new Date(Date.now() - (hours * 3600000));
  return this.find({
    timestamp: { $gte: since }
  })
    .sort({ timestamp: 1 })
    .exec();
};

const SystemStats = mongoose.model('SystemStats', systemStatsSchema);

module.exports = SystemStats;