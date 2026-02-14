from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class ADConnection:
    """Active Directory Connection Manager"""
    
    def __init__(self):
        self.connection = None
        self.server = None
    
    def connect(self, username=None, password=None):
        """Establish connection to AD"""
        try:
            # Get AD configuration from Flask app
            ad_server = current_app.config['AD_SERVER']
            use_ssl = current_app.config['AD_USE_SSL']
            
            # Create server object
            self.server = Server(ad_server, get_info=ALL, use_ssl=use_ssl)
            
            # Use provided credentials or fall back to bind user
            if username and password:
                # Format username for NTLM authentication
                domain = current_app.config['AD_DOMAIN']
                user_dn = f"{domain}\\{username}"
                self.connection = Connection(
                    self.server,
                    user=user_dn,
                    password=password,
                    authentication=NTLM,
                    auto_bind=True
                )
            else:
                # Use configured bind user
                bind_user = current_app.config['AD_BIND_USER']
                bind_password = current_app.config['AD_BIND_PASSWORD']
                self.connection = Connection(
                    self.server,
                    user=bind_user,
                    password=bind_password,
                    auto_bind=True
                )
            
            logger.info("Successfully connected to Active Directory")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to AD: {str(e)}")
            return False
    
    def disconnect(self):
        """Close AD connection"""
        if self.connection:
            self.connection.unbind()
            self.connection = None
    
    def search(self, search_filter, attributes=None, search_base=None):
        """Search AD for objects"""
        if not self.connection:
            return None
        
        if search_base is None:
            search_base = current_app.config['AD_BASE_DN']
        
        try:
            self.connection.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=attributes or ['*']
            )
            return self.connection.entries
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return None
    
    def add_entry(self, dn, object_class, attributes):
        """Add new entry to AD"""
        if not self.connection:
            return False
        
        try:
            self.connection.add(dn, object_class, attributes)
            return self.connection.result['result'] == 0
        except Exception as e:
            logger.error(f"Failed to add entry: {str(e)}")
            return False
    
    def modify_entry(self, dn, changes):
        """Modify existing AD entry"""
        if not self.connection:
            return False
        
        try:
            self.connection.modify(dn, changes)
            return self.connection.result['result'] == 0
        except Exception as e:
            logger.error(f"Failed to modify entry: {str(e)}")
            return False
    
    def delete_entry(self, dn):
        """Delete AD entry"""
        if not self.connection:
            return False
        
        try:
            self.connection.delete(dn)
            return self.connection.result['result'] == 0
        except Exception as e:
            logger.error(f"Failed to delete entry: {str(e)}")
            return False
    
    def get_user(self, username):
        """Get user by sAMAccountName"""
        search_filter = f"(&(objectClass=user)(sAMAccountName={username}))"
        results = self.search(search_filter)
        return results[0] if results else None
    
    def get_group(self, group_name):
        """Get group by name"""
        search_filter = f"(&(objectClass=group)(cn={group_name}))"
        results = self.search(search_filter)
        return results[0] if results else None
    
    def get_computer(self, computer_name):
        """Get computer by name"""
        search_filter = f"(&(objectClass=computer)(cn={computer_name}))"
        results = self.search(search_filter)
        return results[0] if results else None
    
    def add_user_to_group(self, user_dn, group_dn):
        """Add user to group"""
        from ldap3 import MODIFY_ADD
        changes = {'member': [(MODIFY_ADD, [user_dn])]}
        return self.modify_entry(group_dn, changes)
    
    def remove_user_from_group(self, user_dn, group_dn):
        """Remove user from group"""
        from ldap3 import MODIFY_DELETE
        changes = {'member': [(MODIFY_DELETE, [user_dn])]}
        return self.modify_entry(group_dn, changes)

def get_ad_connection(username=None, password=None):
    """Helper function to get AD connection"""
    ad_conn = ADConnection()
    if ad_conn.connect(username, password):
        return ad_conn
    return None
