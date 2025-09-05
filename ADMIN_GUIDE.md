# Biometric Crime Detection System - Admin Guide

## Admin Roles

The system supports two types of administrator roles:

1. **Admin** - Regular administrators who can manage criminal records, perform face and fingerprint matching.
2. **Superadmin** - Higher-level administrators who can do everything regular admins can do, plus manage other administrator accounts.

## Default Login Credentials

### Regular Admin
- **Username**: admin
- **Password**: admin123
- **Capabilities**: Register suspects, view suspects, match faces, match fingerprints

### Superadmin
- **Username**: superadmin
- **Password**: superadmin123
- **Capabilities**: All admin capabilities plus administrator management

## Administrator Management

Superadmins have access to the Administrator Management panel, which can be accessed from the dashboard when logged in as a superadmin. This panel allows superadmins to:

1. **View All Administrators** - See a list of all admin accounts in the system
2. **Add New Administrators** - Create new admin or superadmin accounts
3. **Edit Administrators** - Modify existing administrator details including username, password, and role
4. **Delete Administrators** - Remove administrator accounts from the system

## Security Guidelines

1. Change the default passwords immediately after first login
2. Create only the necessary number of superadmin accounts
3. Regularly review the administrator list to ensure only authorized personnel have access
4. When an administrator leaves the organization, their account should be deleted immediately

## Restrictions

For security reasons, the following restrictions are in place:

1. Administrators cannot delete their own accounts
2. Superadmins cannot downgrade their own role to regular admin
3. Only superadmins can access the administrator management panel

## Troubleshooting

If you encounter issues with administrator access:

1. Ensure you're using the correct username and password
2. Check that the database is properly initialized with the role column
3. If the role column is missing, run the database update script: `python database/update_schema.py`