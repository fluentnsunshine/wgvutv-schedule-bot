from openai import OpenAI
from dotenv import load_dotenv
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from openai import RateLimitError
from tenacity import RetryError

print("Starting OpenAI API key validation test...")

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Basic validation of API key format
if not api_key:
    print("❌ Error: No API key found in .env file")
    print("Make sure you have OPENAI_API_KEY=your-key in your .env file")
elif not api_key.startswith("sk-"):
    print("❌ Error: API key format appears invalid")
    print("OpenAI API keys should start with 'sk-'")
else:
    print("✅ API key found and format appears valid")
    print("Key starts with:", api_key[:7] + "..." + api_key[-4:])
    
    try:
        # Initialize the client
        client = OpenAI(api_key=api_key)
        print("✅ Successfully initialized OpenAI client")
        
        @retry(
            wait=wait_random_exponential(min=1, max=2),
            stop=stop_after_attempt(3),
            retry=retry_if_exception_type(RateLimitError)
        )
        def call_gpt(messages):
            return client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.5
            )
        
        print("\nTrying API call with retry mechanism...")
        messages = [{"role": "user", "content": "Hi"}]
        
        try:
            response = call_gpt(messages)
            print("✅ API call successful!")
            print("Response:", response.choices[0].message.content)
        except RetryError as e:
            print("\n❌ All retry attempts failed!")
            print("Original error:", str(e.last_attempt.exception()))
            if isinstance(e.last_attempt.exception(), RateLimitError):
                print("\nThis appears to be a persistent rate limit error.")
                print("This could mean:")
                print("1. Your account has insufficient quota")
                print("2. Your account has restrictions")
                print("3. The API key is not properly configured")
                print("\nPlease check your account at https://platform.openai.com/account/billing")
            else:
                print("\nThis is not a rate limit error. Please check other possible issues.")
        except Exception as e:
            print("\n❌ Error with API call:", str(e))
            if "429" in str(e):
                print("\nRate limit hit. The retry mechanism will attempt to call again.")
                print("If you're still seeing this error after retries, it might be a quota issue.")
            else:
                print("\nThis is not a rate limit error. Please check other possible issues.")
        
    except Exception as e:
        print("\n❌ Error initializing client:", str(e))
        print("\nDetailed error information:")
        if hasattr(e, 'response'):
            print("Response status:", e.response.status_code)
            print("Response body:", e.response.json())
        print("\nPossible issues:")
        print("1. Check if you have funds in your account at https://platform.openai.com/account/billing")
        print("2. Verify your API key is active at https://platform.openai.com/account/api-keys")
        print("3. Make sure you're using the correct API key format")
        print("4. Check if your account has any restrictions or pending verifications") 