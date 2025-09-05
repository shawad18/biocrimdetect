import React, { useState, useEffect } from 'react';
import api from '../config/api';
import {
  Container,
  Grid,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Box,
  Chip,
  Divider
} from '@mui/material';
import { useTheme } from '@mui/material/styles';

const AdminDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [error, setError] = useState(null);
  const theme = useTheme();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await api.get('/api/admin/dashboard-data');
        setDashboardData(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch dashboard data');
        console.error('Error fetching dashboard data:', err);
      }
    };

    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  if (error) {
    return (
      <Container>
        <Typography color="error" variant="h6" align="center">
          {error}
        </Typography>
      </Container>
    );
  }

  if (!dashboardData) {
    return (
      <Container>
        <Typography variant="h6" align="center">
          Loading...
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* System Stats */}
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: theme.palette.primary.main,
              color: 'white',
            }}
          >
            <Typography component="h2" variant="h6" gutterBottom>
              System Uptime
            </Typography>
            <Typography component="p" variant="h4">
              {dashboardData.uptime}
            </Typography>
          </Paper>
        </Grid>

        {/* Active Users */}
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: theme.palette.success.main,
              color: 'white',
            }}
          >
            <Typography component="h2" variant="h6" gutterBottom>
              Active Users
            </Typography>
            <Typography component="p" variant="h4">
              {dashboardData.activeUsers}
            </Typography>
          </Paper>
        </Grid>

        {/* Failed Logins */}
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: theme.palette.warning.main,
              color: 'white',
            }}
          >
            <Typography component="h2" variant="h6" gutterBottom>
              Failed Logins (24h)
            </Typography>
            <Typography component="p" variant="h4">
              {dashboardData.failedLogins}
            </Typography>
          </Paper>
        </Grid>

        {/* Suspicious Activities */}
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: theme.palette.error.main,
              color: 'white',
            }}
          >
            <Typography component="h2" variant="h6" gutterBottom>
              Suspicious Activities (24h)
            </Typography>
            <Typography component="p" variant="h4">
              {dashboardData.suspiciousActivities}
            </Typography>
          </Paper>
        </Grid>

        {/* Recent Activities Timeline */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography component="h2" variant="h6" gutterBottom>
              Recent Activities
            </Typography>
            <List>
              {dashboardData.recentActivities.map((activity, index) => (
                <React.Fragment key={index}>
                  <ListItem>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="body1">
                            {activity.user} - {activity.action}
                          </Typography>
                          <Chip
                            label={activity.status}
                            size="small"
                            color={
                              activity.status === 'success'
                                ? 'success'
                                : activity.status === 'failed'
                                ? 'error'
                                : activity.status === 'suspicious'
                                ? 'warning'
                                : 'default'
                            }
                          />
                        </Box>
                      }
                      secondary={activity.timestamp}
                    />
                  </ListItem>
                  {index < dashboardData.recentActivities.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default AdminDashboard;