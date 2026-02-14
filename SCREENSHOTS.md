# Screenshots and UI Overview

## Login Page
The login page provides secure authentication using Active Directory credentials.

**Features:**
- Clean, centered login form
- Username and password fields
- Active Directory logo/branding
- Responsive design for mobile and desktop

**URL:** `/auth/login`

---

## Dashboard
The main dashboard provides quick access to all AD management features.

**Features:**
- Welcome message with logged-in user info
- Three main action cards:
  - Users Management
  - Groups Management
  - Computers Management
- Quick action links for common tasks
- Sidebar navigation

**URL:** `/` or `/dashboard`

---

## Users Management

### User List
Browse and search all Active Directory users.

**Features:**
- Searchable user list
- Display: Username, Display Name, Email, Status
- Action buttons: View, Edit
- Create New User button
- Status indicators (Enabled/Disabled)

**URL:** `/users/`

### View User
Display detailed information about a specific user.

**Features:**
- User information panel (username, name, email, etc.)
- Group memberships list
- Action buttons: Edit, Reset Password, Delete
- Distinguished Name (DN) display

**URL:** `/users/view/<username>`

### Create User
Form to create new Active Directory users.

**Features:**
- Required fields: Username, First Name, Last Name, Password
- Optional fields: Email
- Form validation
- Password complexity requirements note

**URL:** `/users/create`

### Edit User
Modify existing user properties.

**Features:**
- Editable fields: Display Name, Email, Description
- Save and Cancel buttons
- Back navigation

**URL:** `/users/edit/<username>`

### Reset Password
Change user password securely.

**Features:**
- Password input field
- Complexity requirements note
- Confirmation workflow

**URL:** `/users/reset-password/<username>`

---

## Groups Management

### Group List
Browse and search all Active Directory groups.

**Features:**
- Searchable group list
- Display: Name, Type, Scope, Member Count, Email
- Type badges (Security/Distribution)
- Action buttons: View, Edit
- Create New Group button

**URL:** `/groups/`

### View Group
Display detailed group information and manage members.

**Features:**
- Group information panel
- Members list with count
- Add member functionality
- Remove member buttons
- Action buttons: Edit, Delete

**URL:** `/groups/view/<group_name>`

### Create Group
Form to create new Active Directory groups.

**Features:**
- Group name input
- Description field
- Group type selection (Security/Distribution)
- Scope selection (Global/Domain Local/Universal)
- Email field for distribution groups

**URL:** `/groups/create`

### Edit Group
Modify existing group properties.

**Features:**
- Description editing
- Email editing
- Save and Cancel buttons

**URL:** `/groups/edit/<group_name>`

---

## Computers Management

### Computer List
Browse and search all Active Directory computer accounts.

**Features:**
- Searchable computer list
- Display: Name, DNS Name, Operating System, Version
- Action buttons: View, Edit
- Search functionality

**URL:** `/computers/`

### View Computer
Display detailed computer information.

**Features:**
- Computer information panel (name, DNS, OS, etc.)
- Group memberships list
- Action buttons: Edit, Delete
- Distinguished Name display

**URL:** `/computers/view/<computer_name>`

### Edit Computer
Modify computer properties.

**Features:**
- Description editing
- Save and Cancel buttons

**URL:** `/computers/edit/<computer_name>`

---

## UI Components

### Navigation Sidebar
Present on all authenticated pages.

**Features:**
- Dashboard link
- Users link
- Groups link
- Computers link
- User info display (username, admin badge)
- Logout button

### Flash Messages
Contextual notifications for user actions.

**Types:**
- Success (green) - Operation completed successfully
- Danger (red) - Error occurred
- Warning (yellow) - Important notice
- Info (blue) - Informational message

### Modals
Confirmation dialogs for destructive actions.

**Used for:**
- Delete User confirmation
- Delete Group confirmation
- Delete Computer confirmation

### Responsive Design
The application uses Bootstrap 5 for responsive design:
- Mobile-friendly navigation
- Responsive tables
- Adaptive layouts for different screen sizes

---

## Color Scheme

- **Primary Color:** Blue (#0d6efd) - Primary actions, links
- **Success Color:** Green (#198754) - Success messages, enabled status
- **Danger Color:** Red (#dc3545) - Errors, delete actions
- **Warning Color:** Yellow (#ffc107) - Warnings
- **Info Color:** Light Blue (#0dcaf0) - Information
- **Secondary Color:** Gray (#6c757d) - Secondary actions

---

## Icons

The application uses Bootstrap Icons for consistent iconography:
- 🏠 `bi-house-door` - Dashboard
- 👥 `bi-people` - Users
- 📚 `bi-collection` - Groups
- 💻 `bi-pc-display` - Computers
- ➕ `bi-plus-circle` - Create/Add
- ✏️ `bi-pencil` - Edit
- 👁️ `bi-eye` - View
- 🗑️ `bi-trash` - Delete
- 🔑 `bi-key` - Password
- 🔒 `bi-shield-lock` - Security
- 🔍 `bi-search` - Search
- ⬅️ `bi-arrow-left` - Back
- 🚪 `bi-box-arrow-right` - Logout

---

## Accessibility

The application follows web accessibility best practices:
- Semantic HTML structure
- ARIA labels where appropriate
- Keyboard navigation support
- High contrast color scheme
- Responsive font sizes
- Screen reader friendly

---

## Browser Compatibility

Tested and compatible with:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## Notes

To capture actual screenshots:
1. Set up a test Active Directory environment
2. Configure the application with AD credentials
3. Run the application: `python app.py`
4. Navigate to `http://localhost:5000`
5. Use browser screenshot tools or screen capture software

For demo purposes without an AD server, you can create mockups or use the templates with sample data.
