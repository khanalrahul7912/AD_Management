# AD Management System

A comprehensive Flask-based web application for managing Active Directory (AD) objects including users, groups, computers, and mailing groups.

## Features

### User Management
- **List and Search Users**: Browse all users or search by username, name, or email
- **Create Users**: Create new AD user accounts with essential attributes
- **View User Details**: See complete user information including group memberships
- **Edit Users**: Modify user properties like display name, email, and description
- **Reset Passwords**: Change user passwords securely
- **Delete Users**: Remove user accounts from Active Directory

### Group Management
- **List and Search Groups**: Browse all groups or search by name
- **Create Groups**: Create security or distribution groups with different scopes (Global, Domain Local, Universal)
- **View Group Details**: See group information and member list
- **Edit Groups**: Modify group properties
- **Manage Members**: Add or remove users from groups
- **Delete Groups**: Remove groups from Active Directory

### Computer Management
- **List and Search Computers**: Browse all computer accounts or search by name
- **View Computer Details**: See computer information including OS, DNS name, and group memberships
- **Edit Computers**: Modify computer properties
- **Delete Computers**: Remove computer accounts

### Security Features
- **Session Management**: Secure session handling with configurable timeouts
- **Authentication**: Login with Active Directory credentials
- **Authorization**: Admin privilege detection and enforcement
- **Password Security**: Secure password handling for AD operations

## Installation

### Prerequisites
- Python 3.7 or higher
- Access to an Active Directory server
- AD credentials with appropriate permissions

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/khanalrahul7912/AD_Management.git
   cd AD_Management
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   ```bash
   cp .env.example .env
   ```
   
   - Edit `.env` and configure your AD settings:
   ```env
   # Flask Configuration
   SECRET_KEY=your-secret-key-here-change-in-production
   FLASK_ENV=development
   
   # Active Directory Configuration
   AD_SERVER=ldap://your-ad-server.domain.com
   AD_DOMAIN=DOMAIN
   AD_BASE_DN=DC=domain,DC=com
   AD_BIND_USER=CN=AD Admin,CN=Users,DC=domain,DC=com
   AD_BIND_PASSWORD=your-admin-password
   AD_USE_SSL=False
   AD_PORT=389
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`
   - Login with your Active Directory credentials

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for session encryption | Random key |
| `FLASK_ENV` | Environment (development/production) | development |
| `AD_SERVER` | LDAP server URL | ldap://localhost |
| `AD_DOMAIN` | Active Directory domain name | DOMAIN |
| `AD_BASE_DN` | Base Distinguished Name for searches | DC=domain,DC=com |
| `AD_BIND_USER` | DN of bind user for AD operations | - |
| `AD_BIND_PASSWORD` | Password for bind user | - |
| `AD_USE_SSL` | Use SSL/TLS for LDAP connection | False |
| `AD_PORT` | LDAP port | 389 (636 for SSL) |
| `SESSION_TYPE` | Session storage type | filesystem |
| `SESSION_PERMANENT` | Make sessions permanent | False |
| `PERMANENT_SESSION_LIFETIME` | Session timeout in seconds | 3600 |

### Security Considerations

1. **Never commit `.env` file**: The `.gitignore` file excludes it
2. **Use strong SECRET_KEY**: Generate using `python -c "import secrets; print(secrets.token_hex(32))"`
3. **Enable SSL in production**: Set `AD_USE_SSL=True` for production
4. **Restrict bind user permissions**: Use least privilege principle
5. **Use HTTPS**: Deploy behind reverse proxy with SSL/TLS

## Project Structure

```
AD_Management/
├── app/
│   ├── __init__.py          # Application factory
│   ├── ad_manager.py        # AD connection and operations
│   ├── auth.py              # Authentication blueprint
│   ├── main.py              # Main/dashboard blueprint
│   ├── users.py             # User management blueprint
│   ├── groups.py            # Group management blueprint
│   ├── computers.py         # Computer management blueprint
│   ├── decorators.py        # Login/admin decorators
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template
│   │   ├── index.html       # Dashboard
│   │   ├── auth/            # Authentication templates
│   │   ├── users/           # User management templates
│   │   ├── groups/          # Group management templates
│   │   └── computers/       # Computer management templates
│   └── static/              # Static files (CSS, JS)
├── app.py                   # Application entry point
├── config.py                # Configuration classes
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Usage

### Login
1. Navigate to the application URL
2. Enter your AD username and password
3. Click "Login"

### Managing Users
- **View Users**: Click "Users" in the sidebar
- **Create User**: Click "Create User" button, fill in the form
- **Search Users**: Use the search box at the top right
- **View Details**: Click the eye icon next to a user
- **Edit User**: Click the pencil icon or "Edit" button
- **Reset Password**: Click "Reset Password" in user details
- **Delete User**: Click "Delete" in user details (confirmation required)

### Managing Groups
- **View Groups**: Click "Groups" in the sidebar
- **Create Group**: Click "Create Group" button, select type and scope
- **Add Members**: In group details, enter username and click "Add"
- **Remove Members**: Click the X button next to a member

### Managing Computers
- **View Computers**: Click "Computers" in the sidebar
- **Search Computers**: Use the search box
- **View/Edit Details**: Click icons next to computer names

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py
```

### Running in Production Mode
```bash
export FLASK_ENV=production  # On Windows: set FLASK_ENV=production
python app.py
```

For production deployment, consider using:
- **Gunicorn** or **uWSGI** as WSGI server
- **Nginx** or **Apache** as reverse proxy
- **Systemd** or **Supervisor** for process management

## Dependencies

- **Flask 3.0.0**: Web framework
- **Flask-Session 0.6.0**: Server-side session management
- **python-dotenv 1.0.0**: Environment variable management
- **ldap3 2.9.1**: LDAP operations
- **Werkzeug 3.0.1**: WSGI utilities

## Troubleshooting

### Cannot connect to AD server
- Verify `AD_SERVER` is correct
- Check network connectivity to AD server
- Ensure firewall allows LDAP traffic (port 389/636)
- Verify bind user credentials

### Login fails
- Ensure username format is correct (without domain prefix)
- Verify user exists in Active Directory
- Check user account is not locked or disabled

### Permission denied errors
- Ensure bind user has sufficient permissions
- Some operations require Domain Admin privileges

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Author

Developed for Active Directory management via web interface.

## Support

For issues and questions, please open an issue on GitHub.