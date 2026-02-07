#!/usr/bin/env python3
"""
Deployment verification script for Chess Training Platform
Checks that all components are properly configured and secure
"""
import sys
import asyncio

async def verify_deployment():
    print("🔍 Chess Training Platform - Deployment Verification\n")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. Check imports
    print("\n1️⃣  Checking imports...")
    try:
        import fastapi
        import uvicorn
        import aiosqlite
        import python_multipart
        from jose import jwt
        from passlib.context import CryptContext
        from app.auth import get_password_hash, create_access_token
        from app.database.database import init_db
        from app.models.schemas import User, Course, Puzzle
        from main import app
        print("   ✅ All imports successful")
    except ImportError as e:
        errors.append(f"Import error: {e}")
        print(f"   ❌ Import failed: {e}")
    
    # 2. Check dependency versions
    print("\n2️⃣  Checking dependency versions...")
    try:
        import fastapi
        import python_multipart
        import jose
        
        versions = {
            'fastapi': fastapi.__version__,
            'python-multipart': python_multipart.__version__,
            'python-jose': jose.__version__
        }
        
        # Verify patched versions
        if versions['fastapi'] >= '0.109.1':
            print(f"   ✅ FastAPI {versions['fastapi']} (patched)")
        else:
            errors.append(f"FastAPI {versions['fastapi']} has vulnerabilities")
            
        if versions['python-multipart'] >= '0.0.22':
            print(f"   ✅ python-multipart {versions['python-multipart']} (patched)")
        else:
            errors.append(f"python-multipart {versions['python-multipart']} has vulnerabilities")
            
        if versions['python-jose'] >= '3.4.0':
            print(f"   ✅ python-jose {versions['python-jose']} (patched)")
        else:
            errors.append(f"python-jose {versions['python-jose']} has vulnerabilities")
            
    except Exception as e:
        errors.append(f"Version check failed: {e}")
    
    # 3. Check file structure
    print("\n3️⃣  Checking file structure...")
    import os
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'SETUP_GUIDE.md',
        'SECURITY.md',
        'app/auth.py',
        'app/database/database.py',
        'app/models/schemas.py',
        'app/templates/index.html',
        'app/static/css/style.css',
        'app/static/js/auth.js'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            errors.append(f"Missing file: {file}")
            print(f"   ❌ Missing: {file}")
    
    # 4. Check environment configuration
    print("\n4️⃣  Checking configuration...")
    if os.path.exists('.env.example'):
        print("   ✅ .env.example exists")
    else:
        warnings.append("No .env.example file found")
    
    if os.path.exists('.env'):
        print("   ⚠️  .env file exists (ensure SECRET_KEY is changed for production)")
        warnings.append("Remember to change SECRET_KEY for production")
    else:
        print("   ℹ️  No .env file (will use .env.example defaults)")
    
    # 5. Test security functions
    print("\n5️⃣  Testing security functions...")
    try:
        from app.auth import get_password_hash, verify_password, create_access_token
        
        # Test password hashing
        test_password = "test_password_123"
        hashed = get_password_hash(test_password)
        if verify_password(test_password, hashed):
            print("   ✅ Password hashing works correctly")
        else:
            errors.append("Password verification failed")
        
        # Test token creation
        token = create_access_token({"sub": "testuser"})
        if token and len(token) > 0:
            print("   ✅ JWT token creation works")
        else:
            errors.append("Token creation failed")
            
    except Exception as e:
        errors.append(f"Security test failed: {e}")
    
    # 6. Check database initialization
    print("\n6️⃣  Testing database...")
    try:
        # Test database connection
        db = await aiosqlite.connect(':memory:')
        await db.execute("SELECT 1")
        await db.close()
        print("   ✅ Database connectivity works")
    except Exception as e:
        errors.append(f"Database test failed: {e}")
    
    # Final report
    print("\n" + "=" * 60)
    print("📊 VERIFICATION RESULTS")
    print("=" * 60)
    
    if not errors and not warnings:
        print("\n✅ ✅ ✅  ALL CHECKS PASSED  ✅ ✅ ✅")
        print("\n🚀 Platform is ready for deployment!")
        return 0
    else:
        if errors:
            print(f"\n❌ ERRORS FOUND ({len(errors)}):")
            for error in errors:
                print(f"   • {error}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for warning in warnings:
                print(f"   • {warning}")
        
        if not errors:
            print("\n✅ No critical errors, but review warnings before deployment")
            return 0
        else:
            print("\n❌ Fix errors before deployment")
            return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(verify_deployment()))
