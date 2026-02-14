from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.decorators import login_required
from app.ad_manager import get_ad_connection
from ldap3 import MODIFY_REPLACE
import secrets
import string

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
@login_required
def list_users():
    """List all users"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('main.index'))
    
    # Search for all users
    search_filter = "(&(objectClass=user)(objectCategory=person))"
    users = ad_conn.search(search_filter, attributes=['sAMAccountName', 'cn', 'mail', 'displayName', 'userAccountControl'])
    
    user_list = []
    if users:
        for user in users:
            try:
                user_data = {
                    'username': user.sAMAccountName.value if hasattr(user, 'sAMAccountName') else '',
                    'name': user.cn.value if hasattr(user, 'cn') else '',
                    'display_name': user.displayName.value if hasattr(user, 'displayName') else '',
                    'email': user.mail.value if hasattr(user, 'mail') else '',
                    'dn': user.entry_dn,
                    'enabled': not (int(user.userAccountControl.value) & 2) if hasattr(user, 'userAccountControl') else True
                }
                user_list.append(user_data)
            except:
                continue
    
    ad_conn.disconnect()
    return render_template('users/list.html', users=user_list)

@users_bp.route('/search')
@login_required
def search_users():
    """Search for users"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('users.list_users'))
    
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('main.index'))
    
    # Search for users matching query
    search_filter = f"(&(objectClass=user)(objectCategory=person)(|(sAMAccountName=*{query}*)(cn=*{query}*)(mail=*{query}*)))"
    users = ad_conn.search(search_filter, attributes=['sAMAccountName', 'cn', 'mail', 'displayName', 'userAccountControl'])
    
    user_list = []
    if users:
        for user in users:
            try:
                user_data = {
                    'username': user.sAMAccountName.value if hasattr(user, 'sAMAccountName') else '',
                    'name': user.cn.value if hasattr(user, 'cn') else '',
                    'display_name': user.displayName.value if hasattr(user, 'displayName') else '',
                    'email': user.mail.value if hasattr(user, 'mail') else '',
                    'dn': user.entry_dn,
                    'enabled': not (int(user.userAccountControl.value) & 2) if hasattr(user, 'userAccountControl') else True
                }
                user_list.append(user_data)
            except:
                continue
    
    ad_conn.disconnect()
    return render_template('users/list.html', users=user_list, query=query)

@users_bp.route('/view/<username>')
@login_required
def view_user(username):
    """View user details"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('users.list_users'))
    
    user = ad_conn.get_user(username)
    if not user:
        flash(f'User {username} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('users.list_users'))
    
    # Get user details
    user_data = {
        'username': user.sAMAccountName.value if hasattr(user, 'sAMAccountName') else '',
        'name': user.cn.value if hasattr(user, 'cn') else '',
        'display_name': user.displayName.value if hasattr(user, 'displayName') else '',
        'email': user.mail.value if hasattr(user, 'mail') else '',
        'description': user.description.value if hasattr(user, 'description') else '',
        'dn': user.entry_dn,
        'member_of': user.memberOf.values if hasattr(user, 'memberOf') and hasattr(user.memberOf, 'values') else [],
        'enabled': not (int(user.userAccountControl.value) & 2) if hasattr(user, 'userAccountControl') else True
    }
    
    ad_conn.disconnect()
    return render_template('users/view.html', user=user_data)

@users_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_user():
    """Create new user"""
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([username, first_name, last_name, password]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('users/create.html')
        
        ad_conn = get_ad_connection(session.get('username'), session.get('password'))
        if not ad_conn:
            flash('Failed to connect to Active Directory.', 'danger')
            return redirect(url_for('users.list_users'))
        
        # Create user DN
        cn = f"{first_name} {last_name}"
        user_dn = f"CN={cn},CN=Users,{ad_conn.connection.server.info.other['defaultNamingContext'][0]}"
        
        # User attributes
        attributes = {
            'sAMAccountName': username,
            'givenName': first_name,
            'sn': last_name,
            'displayName': cn,
            'userPrincipalName': f"{username}@{ad_conn.connection.server.info.other['defaultNamingContext'][0].replace('DC=', '').replace(',', '.')}",
            'userAccountControl': 512  # Normal account
        }
        
        if email:
            attributes['mail'] = email
        
        # Create user
        success = ad_conn.add_entry(user_dn, ['user', 'person', 'organizationalPerson', 'top'], attributes)
        
        if success:
            # Set password
            from ldap3 import MODIFY_REPLACE
            password_value = f'"{password}"'.encode('utf-16-le')
            changes = {'unicodePwd': [(MODIFY_REPLACE, [password_value])]}
            ad_conn.modify_entry(user_dn, changes)
            
            # Enable account
            changes = {'userAccountControl': [(MODIFY_REPLACE, [512])]}
            ad_conn.modify_entry(user_dn, changes)
            
            flash(f'User {username} created successfully.', 'success')
            ad_conn.disconnect()
            return redirect(url_for('users.view_user', username=username))
        else:
            flash('Failed to create user.', 'danger')
        
        ad_conn.disconnect()
    
    return render_template('users/create.html')

@users_bp.route('/edit/<username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    """Edit user details"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('users.list_users'))
    
    user = ad_conn.get_user(username)
    if not user:
        flash(f'User {username} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('users.list_users'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        display_name = request.form.get('display_name')
        description = request.form.get('description')
        
        changes = {}
        if email:
            changes['mail'] = [(MODIFY_REPLACE, [email])]
        if display_name:
            changes['displayName'] = [(MODIFY_REPLACE, [display_name])]
        if description:
            changes['description'] = [(MODIFY_REPLACE, [description])]
        
        if changes:
            success = ad_conn.modify_entry(user.entry_dn, changes)
            if success:
                flash(f'User {username} updated successfully.', 'success')
                ad_conn.disconnect()
                return redirect(url_for('users.view_user', username=username))
            else:
                flash('Failed to update user.', 'danger')
        else:
            flash('No changes to save.', 'info')
        
        ad_conn.disconnect()
        return redirect(url_for('users.view_user', username=username))
    
    # Get user details
    user_data = {
        'username': user.sAMAccountName.value if hasattr(user, 'sAMAccountName') else '',
        'name': user.cn.value if hasattr(user, 'cn') else '',
        'display_name': user.displayName.value if hasattr(user, 'displayName') else '',
        'email': user.mail.value if hasattr(user, 'mail') else '',
        'description': user.description.value if hasattr(user, 'description') else '',
        'dn': user.entry_dn
    }
    
    ad_conn.disconnect()
    return render_template('users/edit.html', user=user_data)

@users_bp.route('/delete/<username>', methods=['POST'])
@login_required
def delete_user(username):
    """Delete user"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('users.list_users'))
    
    user = ad_conn.get_user(username)
    if not user:
        flash(f'User {username} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('users.list_users'))
    
    success = ad_conn.delete_entry(user.entry_dn)
    if success:
        flash(f'User {username} deleted successfully.', 'success')
    else:
        flash('Failed to delete user.', 'danger')
    
    ad_conn.disconnect()
    return redirect(url_for('users.list_users'))

@users_bp.route('/reset-password/<username>', methods=['GET', 'POST'])
@login_required
def reset_password(username):
    """Reset user password"""
    if request.method == 'POST':
        new_password = request.form.get('password')
        
        if not new_password:
            flash('Please provide a password.', 'danger')
            return redirect(url_for('users.view_user', username=username))
        
        ad_conn = get_ad_connection(session.get('username'), session.get('password'))
        if not ad_conn:
            flash('Failed to connect to Active Directory.', 'danger')
            return redirect(url_for('users.list_users'))
        
        user = ad_conn.get_user(username)
        if not user:
            flash(f'User {username} not found.', 'danger')
            ad_conn.disconnect()
            return redirect(url_for('users.list_users'))
        
        # Set new password
        password_value = f'"{new_password}"'.encode('utf-16-le')
        changes = {'unicodePwd': [(MODIFY_REPLACE, [password_value])]}
        success = ad_conn.modify_entry(user.entry_dn, changes)
        
        if success:
            flash(f'Password reset successfully for {username}.', 'success')
        else:
            flash('Failed to reset password.', 'danger')
        
        ad_conn.disconnect()
        return redirect(url_for('users.view_user', username=username))
    
    return render_template('users/reset_password.html', username=username)
