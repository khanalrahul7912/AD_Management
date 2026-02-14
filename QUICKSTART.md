# Quick Start Guide

Get the AD Management System up and running in 5 minutes!

## Prerequisites

- Python 3.7+
- Access to an Active Directory server
- AD credentials with appropriate permissions

## Installation Steps

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/khanalrahul7912/AD_Management.git
cd AD_Management

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your editor
nano .env  # or vim, code, notepad, etc.
```

**Minimum required configuration in `.env`:**

```env
SECRET_KEY=change-this-to-a-random-secret-key
AD_SERVER=ldap://your-ad-server.domain.com
AD_DOMAIN=YOURDOMAIN
AD_BASE_DN=DC=yourdomain,DC=com
AD_BIND_USER=CN=Admin User,CN=Users,DC=yourdomain,DC=com
AD_BIND_PASSWORD=your-admin-password
```

**Quick way to generate a secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

### 4. Login

1. Open your browser and navigate to `http://localhost:5000`
2. Enter your AD username (without domain prefix)
3. Enter your AD password
4. Click "Login"

## Common Configuration Examples

### Example 1: Basic AD Setup

```env
AD_SERVER=ldap://dc01.company.local
AD_DOMAIN=COMPANY
AD_BASE_DN=DC=company,DC=local
AD_BIND_USER=CN=Service Account,CN=Users,DC=company,DC=local
AD_BIND_PASSWORD=P@ssw0rd123
```

### Example 2: AD with SSL

```env
AD_SERVER=ldaps://dc01.company.local
AD_DOMAIN=COMPANY
AD_BASE_DN=DC=company,DC=local
AD_BIND_USER=CN=Service Account,CN=Users,DC=company,DC=local
AD_BIND_PASSWORD=P@ssw0rd123
AD_USE_SSL=True
AD_PORT=636
```

### Example 3: Multiple Domain Controllers

If you have multiple DCs, you can use a load-balanced DNS name or specify the primary:

```env
AD_SERVER=ldap://ad.company.local
```

## Testing the Installation

### Run the Test Suite

```bash
python test_app.py
```

You should see:
```
✓ All tests passed!
```

### Manual Testing

1. **Login Test**
   - Navigate to http://localhost:5000
   - Login with valid AD credentials
   - Verify you see the dashboard

2. **User Management Test**
   - Click "Users" in the sidebar
   - Search for a user
   - View user details

3. **Group Management Test**
   - Click "Groups" in the sidebar
   - View a group
   - Check group members

## Troubleshooting Quick Fixes

### Issue: Cannot connect to AD server

**Solution:**
```bash
# Test AD connectivity
ping your-ad-server.domain.com

# Test LDAP port
telnet your-ad-server.domain.com 389

# Verify DNS resolution
nslookup your-ad-server.domain.com
```

### Issue: Authentication fails

**Possible causes:**
1. Username format - use just the username, not DOMAIN\username
2. Password incorrect
3. Account locked or disabled
4. Bind user credentials wrong

**Solution:**
- Verify bind user can authenticate to AD
- Check bind user has appropriate permissions
- Try logging in with the same credentials on a domain-joined machine

### Issue: Module not found error

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Permission denied errors

**Solution:**
- Verify bind user has permissions to read/modify AD objects
- Check that your account has appropriate permissions
- Some operations require Domain Admin privileges

### Issue: Session errors

**Solution:**
```bash
# Create session directory if it doesn't exist
mkdir -p flask_session

# Or switch to Redis sessions in .env
SESSION_TYPE=redis
```

## Next Steps

- **Read the full documentation:** [README.md](README.md)
- **Deploy to production:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contribute to the project:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **View UI documentation:** [SCREENSHOTS.md](SCREENSHOTS.md)

## Common Tasks

### Create a User
1. Navigate to Users → Create User
2. Fill in required fields (username, first name, last name, password)
3. Optionally add email
4. Click "Create User"

### Add User to Group
1. Navigate to Groups → View Group
2. Enter username in "Add Member" field
3. Click "Add"

### Reset User Password
1. Navigate to Users → View User
2. Click "Reset Password"
3. Enter new password
4. Click "Reset Password"

### Search for Objects
- Use search boxes at the top right of list pages
- Searches work on multiple fields (name, email, description, etc.)

## Security Reminder

⚠️ **Important Security Notes:**

1. Never commit the `.env` file to version control
2. Use a strong, random SECRET_KEY in production
3. Enable SSL/TLS for production deployments
4. Use HTTPS for web access
5. Restrict bind user permissions to minimum required
6. Regularly update dependencies
7. Monitor application logs

## Getting Help

- **Issues:** https://github.com/khanalrahul7912/AD_Management/issues
- **Documentation:** Check README.md and other docs in the repository
- **Community:** Open an issue for questions or discussions

## Quick Commands Reference

```bash
# Activate virtual environment
source venv/bin/activate

# Run application
python app.py

# Run tests
python test_app.py

# Update dependencies
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated

# Deactivate virtual environment
deactivate
```

---

**Congratulations!** You now have a fully functional AD Management System running. 🎉

For production deployment, please refer to [DEPLOYMENT.md](DEPLOYMENT.md) for best practices and advanced configuration.
