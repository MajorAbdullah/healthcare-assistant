import os
from dotenv import load_dotenv

def check_env_file():
    """Check if .env file exists and has required variables."""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Run: cp .env.example .env")
        return False
    
    print("✅ .env file found")
    return True

def check_env_variables():
    """Check if all required environment variables are set."""
    load_dotenv()
    
    required_vars = [
        'PIPEDREAM_PROJECT_ID',
        'PIPEDREAM_ENVIRONMENT',
        'PIPEDREAM_CLIENT_ID',
        'PIPEDREAM_CLIENT_SECRET',
        'GOOGLE_API_KEY',
        'EXTERNAL_USER_ID'
    ]
    
    missing = []
    placeholder_values = ['your_', 'proj_xxxxxxx']
    
    print("\n🔍 Checking environment variables...\n")
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"❌ {var}: Not set")
            missing.append(var)
        elif any(placeholder in value for placeholder in placeholder_values):
            print(f"⚠️  {var}: Using placeholder value (needs updating)")
            missing.append(var)
        else:
            # Show partial value for security
            if 'SECRET' in var or 'KEY' in var:
                display_value = value[:8] + "..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
    
    return len(missing) == 0, missing

def main():
    print("=" * 60)
    print("🔧 ENVIRONMENT CONFIGURATION CHECK")
    print("=" * 60)
    print()
    
    # Check if .env exists
    if not check_env_file():
        return
    
    # Check environment variables
    all_set, missing = check_env_variables()
    
    print()
    print("=" * 60)
    
    if all_set:
        print("✅ All environment variables are configured!")
        print()
        print("🚀 You're ready to run the calendar assistant:")
        print("   python calendar_assistant.py")
    else:
        print("❌ Configuration incomplete!")
        print()
        print("📝 Missing or placeholder variables:")
        for var in missing:
            print(f"   - {var}")
        print()
        print("👉 Edit your .env file and add the required values")
        print()
        print("📚 Where to get credentials:")
        print("   • Pipedream: https://pipedream.com/projects")
        print("   • Google AI: https://ai.google.dev/")
    
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
