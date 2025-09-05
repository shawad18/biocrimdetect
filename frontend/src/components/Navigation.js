import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Security as SecurityIcon
} from '@mui/icons-material';

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <AppBar position="static" sx={{ mb: 3 }}>
      <Container maxWidth="xl">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Biometric Crime Detection
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              color={isActive('/admin/dashboard') ? 'secondary' : 'inherit'}
              startIcon={<DashboardIcon />}
              onClick={() => navigate('/admin/dashboard')}
            >
              Dashboard
            </Button>
            <Button
              color={isActive('/admin/security') ? 'secondary' : 'inherit'}
              startIcon={<SecurityIcon />}
              onClick={() => navigate('/admin/security')}
            >
              Security
            </Button>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navigation;