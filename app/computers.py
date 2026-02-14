from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.decorators import login_required
from app.ad_manager import get_ad_connection
from ldap3 import MODIFY_REPLACE

computers_bp = Blueprint('computers', __name__)

@computers_bp.route('/')
@login_required
def list_computers():
    """List all computers"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('main.index'))
    
    # Search for all computers
    search_filter = "(objectClass=computer)"
    computers = ad_conn.search(search_filter, attributes=['cn', 'description', 'operatingSystem', 'operatingSystemVersion', 'dNSHostName', 'lastLogon'])
    
    computer_list = []
    if computers:
        for computer in computers:
            try:
                computer_data = {
                    'name': computer.cn.value if hasattr(computer, 'cn') else '',
                    'description': computer.description.value if hasattr(computer, 'description') else '',
                    'os': computer.operatingSystem.value if hasattr(computer, 'operatingSystem') else '',
                    'os_version': computer.operatingSystemVersion.value if hasattr(computer, 'operatingSystemVersion') else '',
                    'dns_name': computer.dNSHostName.value if hasattr(computer, 'dNSHostName') else '',
                    'dn': computer.entry_dn
                }
                computer_list.append(computer_data)
            except:
                continue
    
    ad_conn.disconnect()
    return render_template('computers/list.html', computers=computer_list)

@computers_bp.route('/search')
@login_required
def search_computers():
    """Search for computers"""
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('computers.list_computers'))
    
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('main.index'))
    
    # Search for computers matching query
    search_filter = f"(&(objectClass=computer)(|(cn=*{query}*)(description=*{query}*)(dNSHostName=*{query}*)))"
    computers = ad_conn.search(search_filter, attributes=['cn', 'description', 'operatingSystem', 'operatingSystemVersion', 'dNSHostName'])
    
    computer_list = []
    if computers:
        for computer in computers:
            try:
                computer_data = {
                    'name': computer.cn.value if hasattr(computer, 'cn') else '',
                    'description': computer.description.value if hasattr(computer, 'description') else '',
                    'os': computer.operatingSystem.value if hasattr(computer, 'operatingSystem') else '',
                    'os_version': computer.operatingSystemVersion.value if hasattr(computer, 'operatingSystemVersion') else '',
                    'dns_name': computer.dNSHostName.value if hasattr(computer, 'dNSHostName') else '',
                    'dn': computer.entry_dn
                }
                computer_list.append(computer_data)
            except:
                continue
    
    ad_conn.disconnect()
    return render_template('computers/list.html', computers=computer_list, query=query)

@computers_bp.route('/view/<computer_name>')
@login_required
def view_computer(computer_name):
    """View computer details"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('computers.list_computers'))
    
    computer = ad_conn.get_computer(computer_name)
    if not computer:
        flash(f'Computer {computer_name} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('computers.list_computers'))
    
    # Get computer details
    computer_data = {
        'name': computer.cn.value if hasattr(computer, 'cn') else '',
        'description': computer.description.value if hasattr(computer, 'description') else '',
        'os': computer.operatingSystem.value if hasattr(computer, 'operatingSystem') else '',
        'os_version': computer.operatingSystemVersion.value if hasattr(computer, 'operatingSystemVersion') else '',
        'dns_name': computer.dNSHostName.value if hasattr(computer, 'dNSHostName') else '',
        'dn': computer.entry_dn,
        'member_of': computer.memberOf.values if hasattr(computer, 'memberOf') and hasattr(computer.memberOf, 'values') else []
    }
    
    ad_conn.disconnect()
    return render_template('computers/view.html', computer=computer_data)

@computers_bp.route('/edit/<computer_name>', methods=['GET', 'POST'])
@login_required
def edit_computer(computer_name):
    """Edit computer details"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('computers.list_computers'))
    
    computer = ad_conn.get_computer(computer_name)
    if not computer:
        flash(f'Computer {computer_name} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('computers.list_computers'))
    
    if request.method == 'POST':
        description = request.form.get('description')
        
        changes = {}
        if description:
            changes['description'] = [(MODIFY_REPLACE, [description])]
        
        if changes:
            success = ad_conn.modify_entry(computer.entry_dn, changes)
            if success:
                flash(f'Computer {computer_name} updated successfully.', 'success')
                ad_conn.disconnect()
                return redirect(url_for('computers.view_computer', computer_name=computer_name))
            else:
                flash('Failed to update computer.', 'danger')
        else:
            flash('No changes to save.', 'info')
        
        ad_conn.disconnect()
        return redirect(url_for('computers.view_computer', computer_name=computer_name))
    
    # Get computer details
    computer_data = {
        'name': computer.cn.value if hasattr(computer, 'cn') else '',
        'description': computer.description.value if hasattr(computer, 'description') else '',
        'dn': computer.entry_dn
    }
    
    ad_conn.disconnect()
    return render_template('computers/edit.html', computer=computer_data)

@computers_bp.route('/delete/<computer_name>', methods=['POST'])
@login_required
def delete_computer(computer_name):
    """Delete computer"""
    ad_conn = get_ad_connection(session.get('username'), session.get('password'))
    if not ad_conn:
        flash('Failed to connect to Active Directory.', 'danger')
        return redirect(url_for('computers.list_computers'))
    
    computer = ad_conn.get_computer(computer_name)
    if not computer:
        flash(f'Computer {computer_name} not found.', 'danger')
        ad_conn.disconnect()
        return redirect(url_for('computers.list_computers'))
    
    success = ad_conn.delete_entry(computer.entry_dn)
    if success:
        flash(f'Computer {computer_name} deleted successfully.', 'success')
    else:
        flash('Failed to delete computer.', 'danger')
    
    ad_conn.disconnect()
    return redirect(url_for('computers.list_computers'))
