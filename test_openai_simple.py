from openai import OpenAI
from dotenv import load_dotenv
import os
import json

def print_error_details(error):
    """Print detailed error information in a readable format."""
    print("\n🔍 Detailed Error Information:")
    print("-" * 50)
    print(f"Error Type: {type(error).__name__}")
    print(f"Error Message: {str(error)}")
    
    if hasattr(error, 'response'):
        print("\nResponse Details:")
        print(f"Status Code: {error.response.status_code}")
        try:
            error_body = error.response.json()
            print("Error Body:")
            print(json.dumps(error_body, indent=2))
        except:
            print("Could not parse error body as JSON")
    
    print("\n🔧 Troubleshooting Steps:")
    print("1. Verify API Key Format:")
    print("   - Should start with 'sk-'")
    print("   - Should be a valid API key from OpenAI")
    print("2. Check Account Status:")
    print("   - Visit https://platform.openai.com/account/billing")
    print("   - Verify account has funds")
    print("   - Check for any restrictions")
    print("3. API Key Status:")
    print("   - Visit https://platform.openai.com/account/api-keys")
    print("   - Verify key is active")
    print("   - Check key permissions")
    print("-" * 50)

def test_lm_studio():
    """Test connection to local LM Studio model."""
    print("\n🔄 Testing LM Studio Connection")
    
    try:
        # Initialize client with LM Studio base URL
        client = OpenAI(
            base_url="http://127.0.0.1:1234/v1",  # Updated to use 127.0.0.1
            api_key="not-needed"  # LM Studio doesn't need an API key
        )
        print("✅ Successfully initialized LM Studio client")
        
        # Test chat completion
        print("\n🔄 Testing Chat Completion")
        try:
            response = client.chat.completions.create(
                model="qwen2.5-7b-instruct-1m",  # Updated to use your specific model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say hello!"}
                ],
                max_tokens=50,
                temperature=0.7
            )
            print("✅ Success!")
            print(f"Response: {response.choices[0].message.content}")
            return True
        except Exception as e:
            print("❌ Failed!")
            print_error_details(e)
            return False
            
    except Exception as e:
        print("\n❌ Failed to initialize LM Studio client!")
        print_error_details(e)
        return False

def test_openai_api():
    """Test OpenAI API connection with multiple approaches."""
    print("🚀 Starting OpenAI API Connection Test")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: No API key found in .env file")
        return
    
    print(f"\n📝 API Key Format Check:")
    print(f"Key starts with 'sk-': {'✅' if api_key.startswith('sk-') else '❌'}")
    print(f"Key length: {len(api_key)} characters")
    
    try:
        # Initialize client
        client = OpenAI(api_key=api_key)
        print("\n✅ Successfully initialized OpenAI client")
        
        # Test 1: Simple completion
        print("\n🔄 Test 1: Simple Completion")
        try:
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt="Say hello!",
                max_tokens=5
            )
            print("✅ Success!")
            print(f"Response: {response.choices[0].text.strip()}")
        except Exception as e:
            print("❌ Failed!")
            print_error_details(e)
        
        # Test 2: Chat completion with minimal parameters
        print("\n🔄 Test 2: Chat Completion (Minimal)")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say hello!"}]
            )
            print("✅ Success!")
            print(f"Response: {response.choices[0].message.content}")
        except Exception as e:
            print("❌ Failed!")
            print_error_details(e)
        
        # Test 3: Chat completion with full parameters
        print("\n🔄 Test 3: Chat Completion (Full Parameters)")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say hello!"}],
                max_tokens=50,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print("✅ Success!")
            print(f"Response: {response.choices[0].message.content}")
        except Exception as e:
            print("❌ Failed!")
            print_error_details(e)
            
    except Exception as e:
        print("\n❌ Failed to initialize OpenAI client!")
        print_error_details(e)

if __name__ == "__main__":
    print("🤖 AI Model Connection Tests")
    print("=" * 50)
    
    # Test LM Studio first
    if test_lm_studio():
        print("\n✅ LM Studio test completed successfully!")
    else:
        print("\n❌ LM Studio test failed. Make sure LM Studio is running and a model is loaded.")
    
    # Then test OpenAI API
    test_openai_api() 