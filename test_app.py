#!/usr/bin/env python3
"""
Test script for AD Management Application
This script validates the application structure and basic functionality.
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from app import create_app
        from app.ad_manager import ADConnection, get_ad_connection
        from app.decorators import login_required, admin_required
        from config import Config, DevelopmentConfig, ProductionConfig
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_creation():
    """Test application creation"""
    print("\nTesting application creation...")
    try:
        from app import create_app
        app = create_app()
        print("✓ Application created successfully")
        return True
    except Exception as e:
        print(f"✗ Application creation error: {e}")
        return False

def test_routes():
    """Test that all expected routes are registered"""
    print("\nTesting routes...")
    try:
        from app import create_app
        app = create_app()
        
        expected_routes = [
            'main.index',
            'auth.login',
            'auth.logout',
            'users.list_users',
            'users.create_user',
            'users.view_user',
            'users.edit_user',
            'users.delete_user',
            'users.reset_password',
            'groups.list_groups',
            'groups.create_group',
            'groups.view_group',
            'groups.edit_group',
            'groups.delete_group',
            'groups.add_member',
            'groups.remove_member',
            'computers.list_computers',
            'computers.view_computer',
            'computers.edit_computer',
            'computers.delete_computer'
        ]
        
        registered_endpoints = [rule.endpoint for rule in app.url_map.iter_rules()]
        
        missing = []
        for route in expected_routes:
            if route not in registered_endpoints:
                missing.append(route)
        
        if missing:
            print(f"✗ Missing routes: {', '.join(missing)}")
            return False
        else:
            print(f"✓ All {len(expected_routes)} expected routes are registered")
            return True
    except Exception as e:
        print(f"✗ Route testing error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    try:
        from config import Config, DevelopmentConfig, ProductionConfig
        
        # Test development config
        dev_config = DevelopmentConfig()
        assert dev_config.DEBUG == True
        assert dev_config.FLASK_ENV == 'development'
        
        # Test production config
        prod_config = ProductionConfig()
        assert prod_config.DEBUG == False
        assert prod_config.FLASK_ENV == 'production'
        
        print("✓ Configuration classes working correctly")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_templates():
    """Test that all required templates exist"""
    print("\nTesting templates...")
    try:
        required_templates = [
            'app/templates/base.html',
            'app/templates/index.html',
            'app/templates/dashboard.html',
            'app/templates/auth/login.html',
            'app/templates/users/list.html',
            'app/templates/users/view.html',
            'app/templates/users/create.html',
            'app/templates/users/edit.html',
            'app/templates/users/reset_password.html',
            'app/templates/groups/list.html',
            'app/templates/groups/view.html',
            'app/templates/groups/create.html',
            'app/templates/groups/edit.html',
            'app/templates/computers/list.html',
            'app/templates/computers/view.html',
            'app/templates/computers/edit.html'
        ]
        
        missing = []
        for template in required_templates:
            if not os.path.exists(template):
                missing.append(template)
        
        if missing:
            print(f"✗ Missing templates: {', '.join(missing)}")
            return False
        else:
            print(f"✓ All {len(required_templates)} required templates exist")
            return True
    except Exception as e:
        print(f"✗ Template testing error: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are installed"""
    print("\nTesting dependencies...")
    try:
        import flask
        import flask_session
        import dotenv
        import ldap3
        import werkzeug
        
        print("✓ All required dependencies are installed")
        print(f"  - Flask: {flask.__version__}")
        print(f"  - ldap3: {ldap3.__version__}")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("AD Management Application - Test Suite")
    print("=" * 60)
    
    tests = [
        test_dependencies,
        test_imports,
        test_config,
        test_app_creation,
        test_routes,
        test_templates
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
