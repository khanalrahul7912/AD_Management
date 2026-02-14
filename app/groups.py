from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.decorators import login_required
from app.ad_manager import get_ad_connection
from ldap3 import MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/')
@login_required
def list_groups():
    """List all groups"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('main.index'))
    
    # Search for all groups
    search_filter = "(objectClass=group)"
    groups = ad_conn.search(search_filter, attributes=['cn', 'description', 'member', 'groupType', 'mail'])
    
    group_list = []
    if groups:
        for group in groups:
            try:
                members = group.member.values if hasattr(group, 'member') and hasattr(group.member, 'values') else []
                group_type = int(group.groupType.value) if hasattr(group, 'groupType') else 0
                
                # Determine group scope and type
                is_security = bool(group_type & 0x80000000)
                scope = 'Unknown'
                if group_type & 2:
                    scope = 'Global'
                elif group_type & 4:
                    scope = 'Domain Local'
                elif group_type & 8:
                    scope = 'Universal'
                
                group_data = {
                    'name': group.cn.value if hasattr(group, 'cn') else '',
                    'description': group.description.value if hasattr(group, 'description') else '',
                    'dn': group.entry_dn,
                    'member_count': len(members),
                    'type': 'Security' if is_security else 'Distribution',
                    'scope': scope,
                    'email': group.mail.value if hasattr(group, 'mail') else ''
                }
                group_list.append(group_data)
            except:
                continue
    
    ad_conn.disconnect()
    return render_template('groups/list.html', groups=group_list)

@groups_bp.route('/search')
@login_required
def search_groups():
    """Search for groups"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('groups.list_groups'))
    
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('main.index'))
    
    # Search for groups matching query
    search_filter = f"(&(objectClass=group)(|(cn=*{query}*)(description=*{query}*)))"
    groups = ad_conn.search(search_filter, attributes=['cn', 'description', 'member', 'groupType', 'mail'])
    
    group_list = []
    if groups:
        for group in groups:
            try:
                members = group.member.values if hasattr(group, 'member') and hasattr(group.member, 'values') else []
                group_type = int(group.groupType.value) if hasattr(group, 'groupType') else 0
                
                is_security = bool(group_type & 0x80000000)
                scope = 'Unknown'
                if group_type & 2:
                    scope = 'Global'
                elif group_type & 4:
                    scope = 'Domain Local'
                elif group_type & 8:
                    scope = 'Universal'
                
                group_data = {
                    'name': group.cn.value if hasattr(group, 'cn') else '',
                    'description': group.description.value if hasattr(group, 'description') else '',
                    'dn': group.entry_dn,
                    'member_count': len(members),
                    'type': 'Security' if is_security else 'Distribution',
                    'scope': scope,
                    'email': group.mail.value if hasattr(group, 'mail') else ''
                }
                group_list.append(group_data)
            except:
                continue
    
    ad_conn.disconnect()
    return render_template('groups/list.html', groups=group_list, query=query)

@groups_bp.route('/view/<group_name>')
@login_required
def view_group(group_name):
    """View group details"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('groups.list_groups'))
    
    group = ad_conn.get_group(group_name)
    if not group:
        flash(f'Group {group_name} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('groups.list_groups'))
    
    # Get group details
    members = group.member.values if hasattr(group, 'member') and hasattr(group.member, 'values') else []
    group_type = int(group.groupType.value) if hasattr(group, 'groupType') else 0
    
    is_security = bool(group_type & 0x80000000)
    scope = 'Unknown'
    if group_type & 2:
        scope = 'Global'
    elif group_type & 4:
        scope = 'Domain Local'
    elif group_type & 8:
        scope = 'Universal'
    
    # Get member details
    member_list = []
    for member_dn in members:
        # Extract CN from DN
        cn = member_dn.split(',')[0].replace('CN=', '')
        member_list.append({'dn': member_dn, 'name': cn})
    
    group_data = {
        'name': group.cn.value if hasattr(group, 'cn') else '',
        'description': group.description.value if hasattr(group, 'description') else '',
        'dn': group.entry_dn,
        'members': member_list,
        'type': 'Security' if is_security else 'Distribution',
        'scope': scope,
        'email': group.mail.value if hasattr(group, 'mail') else ''
    }
    
    ad_conn.disconnect()
    return render_template('groups/view.html', group=group_data)

@groups_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_group():
    """Create new group"""
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        description = request.form.get('description')
        group_type = request.form.get('group_type', 'security')
        scope = request.form.get('scope', 'global')
        email = request.form.get('email')
        
        if not group_name:
            flash('Please provide a group name.', 'danger')
            return render_template('groups/create.html')
        
        ad_conn = get_ad_connection(session.get('username'), session.get('password'))
        if not ad_conn:
            flash('Failed to connect to Active Directory.', 'danger')
            return redirect(url_for('groups.list_groups'))
        
        # Create group DN
        group_dn = f"CN={group_name},CN=Users,{ad_conn.connection.server.info.other['defaultNamingContext'][0]}"
        
        # Calculate groupType value
        group_type_value = 0
        if scope == 'global':
            group_type_value = 2
        elif scope == 'domain_local':
            group_type_value = 4
        elif scope == 'universal':
            group_type_value = 8
        
        if group_type == 'security':
            group_type_value |= 0x80000000
        
        # Group attributes
        attributes = {
            'sAMAccountName': group_name,
            'groupType': group_type_value
        }
        
        if description:
            attributes['description'] = description
        
        if email and group_type == 'distribution':
            attributes['mail'] = email
        
        # Create group
        success = ad_conn.add_entry(group_dn, ['group', 'top'], attributes)
        
        if success:
            flash(f'Group {group_name} created successfully.', 'success')
            ad_conn.disconnect()
            return redirect(url_for('groups.view_group', group_name=group_name))
        else:
            flash('Failed to create group.', 'danger')
        
        ad_conn.disconnect()
    
    return render_template('groups/create.html')

@groups_bp.route('/edit/<group_name>', methods=['GET', 'POST'])
@login_required
def edit_group(group_name):
    """Edit group details"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('groups.list_groups'))
    
    group = ad_conn.get_group(group_name)
    if not group:
        flash(f'Group {group_name} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('groups.list_groups'))
    
    if request.method == 'POST':
        description = request.form.get('description')
        email = request.form.get('email')
        
        changes = {}
        if description:
            changes['description'] = [(MODIFY_REPLACE, [description])]
        if email:
            changes['mail'] = [(MODIFY_REPLACE, [email])]
        
        if changes:
            success = ad_conn.modify_entry(group.entry_dn, changes)
            if success:
                flash(f'Group {group_name} updated successfully.', 'success')
                ad_conn.disconnect()
                return redirect(url_for('groups.view_group', group_name=group_name))
            else:
                flash('Failed to update group.', 'danger')
        else:
            flash('No changes to save.', 'info')
        
        ad_conn.disconnect()
        return redirect(url_for('groups.view_group', group_name=group_name))
    
    # Get group details
    group_data = {
        'name': group.cn.value if hasattr(group, 'cn') else '',
        'description': group.description.value if hasattr(group, 'description') else '',
        'email': group.mail.value if hasattr(group, 'mail') else '',
        'dn': group.entry_dn
    }
    
    ad_conn.disconnect()
    return render_template('groups/edit.html', group=group_data)

@groups_bp.route('/delete/<group_name>', methods=['POST'])
@login_required
def delete_group(group_name):
    """Delete group"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('groups.list_groups'))
    
    group = ad_conn.get_group(group_name)
    if not group:
        flash(f'Group {group_name} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('groups.list_groups'))
    
    success = ad_conn.delete_entry(group.entry_dn)
    if success:
        flash(f'Group {group_name} deleted successfully.', 'success')
    else:
        flash('Failed to delete group.', 'danger')
    
    ad_conn.disconnect()
    return redirect(url_for('groups.list_groups'))

@groups_bp.route('/<group_name>/add-member', methods=['POST'])
@login_required
def add_member(group_name):
    """Add member to group"""
    username = request.form.get('username')
    
    if not username:
        flash('Please provide a username.', 'danger')
        return redirect(url_for('groups.view_group', group_name=group_name))
    
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('groups.list_groups'))
    
    # Get user and group
    user = ad_conn.get_user(username)
    group = ad_conn.get_group(group_name)
    
    if not user:
        flash(f'User {username} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('groups.view_group', group_name=group_name))
    
    if not group:
        flash(f'Group {group_name} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('groups.list_groups'))
    
    # Add user to group
    success = ad_conn.add_user_to_group(user.entry_dn, group.entry_dn)
    
    if success:
        flash(f'User {username} added to {group_name} successfully.', 'success')
    else:
        flash('Failed to add user to group.', 'danger')
    
    ad_conn.disconnect()
    return redirect(url_for('groups.view_group', group_name=group_name))

@groups_bp.route('/<group_name>/remove-member', methods=['POST'])
@login_required
def remove_member(group_name):
    """Remove member from group"""
    member_dn = request.form.get('member_dn')
    
    if not member_dn:
        flash('Invalid member.', 'danger')
        return redirect(url_for('groups.view_group', group_name=group_name))
    
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('groups.list_groups'))
    
    group = ad_conn.get_group(group_name)
    if not group:
        flash(f'Group {group_name} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('groups.list_groups'))
    
    # Remove user from group
    success = ad_conn.remove_user_from_group(member_dn, group.entry_dn)
    
    if success:
        flash('Member removed from group successfully.', 'success')
    else:
        flash('Failed to remove member from group.', 'danger')
    
    ad_conn.disconnect()
    return redirect(url_for('groups.view_group', group_name=group_name))
