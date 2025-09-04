from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from models.user import User
from models.activity_log import ActivityLog
from utils.auth import admin_required
import psutil

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/dashboard-data')
@admin_required
def get_dashboard_data():
    try:
        # Get system uptime
        uptime = str(timedelta(seconds=int(psutil.boot_time())))
        
        # Get active users count (users who logged in within the last 30 minutes)
        active_users = User.query.filter(
            User.last_login >= datetime.utcnow() - timedelta(minutes=30)
        ).count()
        
        # Get failed login attempts in the last 24 hours
        failed_logins = ActivityLog.query.filter(
            ActivityLog.action == 'login',
            ActivityLog.status == 'failed',
            ActivityLog.timestamp >= datetime.utcnow() - timedelta(hours=24)
        ).count()
        
        # Get suspicious activities count
        suspicious_activities = ActivityLog.query.filter(
            ActivityLog.status == 'suspicious',
            ActivityLog.timestamp >= datetime.utcnow() - timedelta(hours=24)
        ).count()
        
        # Get recent activities
        recent_activities = ActivityLog.query.order_by(
            ActivityLog.timestamp.desc()
        ).limit(10).all()
        
        activities_list = [{
            'timestamp': activity.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'user': activity.user.username if activity.user else 'System',
            'action': activity.action,
            'status': activity.status
        } for activity in recent_activities]
        
        return jsonify({
            'uptime': uptime,
            'activeUsers': active_users,
            'failedLogins': failed_logins,
            'suspiciousActivities': suspicious_activities,
            'recentActivities': activities_list
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500