const os = require('os');
const si = require('systeminformation');
const SystemStats = require('../models/SystemStats');

class SystemMonitor {
  constructor() {
    this.updateInterval = 60000; // Update every minute
    this.intervalId = null;
  }

  start() {
    this.collectStats(); // Initial collection
    this.intervalId = setInterval(() => this.collectStats(), this.updateInterval);
    console.log('System monitoring service started');
  }

  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      console.log('System monitoring service stopped');
    }
  }

  async collectStats() {
    try {
      const stats = {
        timestamp: new Date(),
        uptime: this.formatUptime(os.uptime()),
        cpuUsage: await this.getCpuUsage(),
        memoryUsage: this.getMemoryUsage(),
        diskUsage: await this.getDiskUsage(),
        networkStats: await this.getNetworkStats(),
        activeConnections: await this.getActiveConnections()
      };

      await SystemStats.create(stats);

      // Keep only last 24 hours of stats
      const twentyFourHoursAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
      await SystemStats.deleteMany({ timestamp: { $lt: twentyFourHoursAgo } });

    } catch (error) {
      console.error('Error collecting system stats:', error);
    }
  }

  formatUptime(seconds) {
    const days = Math.floor(seconds / (24 * 60 * 60));
    const hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60));
    const minutes = Math.floor((seconds % (60 * 60)) / 60);
    const remainingSeconds = Math.floor(seconds % 60);

    return `${days}d ${hours}h ${minutes}m ${remainingSeconds}s`;
  }

  async getCpuUsage() {
    try {
      const cpuLoad = await si.currentLoad();
      return cpuLoad.currentLoad.toFixed(2);
    } catch (error) {
      console.error('Error getting CPU usage:', error);
      return '0.00';
    }
  }

  getMemoryUsage() {
    const total = os.totalmem();
    const free = os.freemem();
    const used = total - free;
    const percentUsed = ((used / total) * 100).toFixed(2);

    return {
      total,
      used,
      free,
      percentUsed: parseFloat(percentUsed)
    };
  }

  async getDiskUsage() {
    try {
      const disks = await si.fsSize();
      if (disks.length > 0) {
        const mainDisk = disks[0];
        return {
          total: mainDisk.size,
          used: mainDisk.used,
          free: mainDisk.available,
          percentUsed: parseFloat(mainDisk.use.toFixed(2))
        };
      }
      return { total: 0, used: 0, free: 0, percentUsed: 0 };
    } catch (error) {
      console.error('Error getting disk usage:', error);
      return { total: 0, used: 0, free: 0, percentUsed: 0 };
    }
  }

  async getNetworkStats() {
    try {
      const networkStats = await si.networkStats();
      if (networkStats.length > 0) {
        const mainInterface = networkStats[0];
        return {
          bytesReceived: mainInterface.rx_bytes || 0,
          bytesSent: mainInterface.tx_bytes || 0,
          packetsReceived: mainInterface.rx_sec || 0,
          packetsSent: mainInterface.tx_sec || 0
        };
      }
      return { bytesReceived: 0, bytesSent: 0, packetsReceived: 0, packetsSent: 0 };
    } catch (error) {
      console.error('Error getting network stats:', error);
      return { bytesReceived: 0, bytesSent: 0, packetsReceived: 0, packetsSent: 0 };
    }
  }

  async getActiveConnections() {
    try {
      const connections = await si.networkConnections();
      return connections.filter(conn => conn.state === 'ESTABLISHED').length;
    } catch (error) {
      console.error('Error getting active connections:', error);
      return 0;
    }
  }
}

module.exports = new SystemMonitor();