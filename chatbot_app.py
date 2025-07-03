import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI
from typing import Tuple, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client with LM Studio
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"  # LM Studio doesn't need an API key
)

# Set page config
st.set_page_config(
    page_title="WGVU TV Schedule Assistant",
    page_icon="📺",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stMarkdown {
        font-size: 16px;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e6f3ff;
    }
    .assistant-message {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

def load_schedules() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Load both schedule files and handle errors."""
    try:
        override_df = pd.read_excel('schedule_override.xlsx')
        regular_df = pd.read_excel('sample_tv_schedule_with_dates.xlsx')
        return override_df, regular_df
    except FileNotFoundError as e:
        st.error("Error: Could not find schedule files. Please make sure both schedule files exist.")
        return None, None

def test_lm_studio_connection():
    """Test if LM Studio is accessible."""
    try:
        response = client.chat.completions.create(
            model="phi-3.1-mini-128k-instruct",
            messages=[
                {"role": "system", "content": "Test connection"},
                {"role": "user", "content": "Test"}
            ],
            max_tokens=5
        )
        return True
    except Exception as e:
        st.error(f"❌ Cannot connect to LM Studio: {str(e)}")
        return False

def extract_show_title(query: str) -> str:
    """Use LM Studio to extract the show title from the user's query."""
    try:
        response = client.chat.completions.create(
            model="phi-3.1-mini-128k-instruct",
            messages=[
                {"role": "system", "content": "Extract ONLY the TV show title from the user's message. Respond with ONLY the show title. No explanation. No reasoning. Just the title."},
                {"role": "user", "content": query}
            ],
            max_tokens=50,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"❌ Error with LM Studio: {str(e)}")
        return query

def search_schedule(title: str, override_df: pd.DataFrame, regular_df: pd.DataFrame) -> Tuple[pd.DataFrame, str]:
    """Search for a show in both schedules."""
    title = title.lower()
    
    # Search in override schedule
    override_matches = override_df[override_df['Program Title'].fillna('').str.lower().str.contains(title)]
    if not override_matches.empty:
        return override_matches, "Override"
    
    # Search in regular schedule
    regular_matches = regular_df[regular_df['Program Title'].fillna('').str.lower().str.contains(title)]
    if not regular_matches.empty:
        return regular_matches, "Regular"
    
    return pd.DataFrame(), "None"

def format_schedule_result(row: pd.Series) -> str:
    """Format a single schedule result into a readable string."""
    try:
        date = pd.to_datetime(row['Date']).strftime("%A, %B %d")
        start = pd.to_datetime(str(row['Start Time'])).strftime("%I:%M %p")
        end = pd.to_datetime(str(row['End Time'])).strftime("%I:%M %p")
        
        return (f"📺 {row['Program Title']} on {row['Channel Name']}\n"
                f"🗓️ {date}\n"
                f"⏰ {start} – {end}")
    except Exception as e:
        st.error(f"Error formatting schedule: {str(e)}")
        return f"📺 {row['Program Title']} on {row['Channel Name']}"

def main():
    # Initialize session state for chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Test LM Studio connection
    if not test_lm_studio_connection():
        st.error("⚠️ LM Studio is not responding. Please make sure it's running and try again.")
        return
    
    # Header
    st.title("📺 WGVU TV Schedule Assistant")
    st.markdown("""
        Hi! I'm your TV schedule assistant. Ask me about any show and I'll tell you when it's airing on WGVU.
        You can ask questions like:
        - "When is Arthur on?"
        - "What time is American Experience?"
        - "Show me the schedule for Nature"
    """)
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()  # Keep this one as it's needed for clearing the chat
    
    # Load schedules
    override_df, regular_df = load_schedules()
    if override_df is None or regular_df is None:
        st.error("❌ I couldn't load the TV schedules. Please make sure the schedule files are in the correct location.")
        return
    
    # Create a container for chat messages
    chat_container = st.empty()
    
    # Display chat history
    with chat_container.container():
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # Chat input form
    with st.form("chat_form"):
        user_input = st.text_input("🎯 Ask about a TV show...", placeholder="When is Arthur on?")
        submitted = st.form_submit_button("Send")
        
        if submitted:
            st.write("Debug - Form submitted")  # Debug info
            st.write("Debug - User input:", user_input)  # Debug info
            
            if user_input:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.write("Debug - Added user message to history")  # Debug info
                
                with st.spinner("Let me check the schedule for you..."):
                    try:
                        # Extract show title using LM Studio
                        show_title = extract_show_title(user_input)
                        st.write("Debug - Extracted title:", show_title)  # Debug info
                        
                        # Search schedules
                        results, source = search_schedule(show_title, override_df, regular_df)
                        st.write("Debug - Found matches:", len(results))  # Debug info
                        st.write("Debug - Source:", source)  # Debug info
                        
                        # Prepare response
                        if not results.empty:
                            response = f"Great news! I found {len(results)} airing{'s' if len(results) > 1 else ''} of {show_title}:\n\n"
                            for _, row in results.iterrows():
                                response += format_schedule_result(row) + "\n\n"
                            response += "Hope this helps! Let me know if you'd like to know about any other shows."
                        else:
                            response = f"I couldn't find any upcoming airings of {show_title}. "
                            response += "Would you like to try searching for a different show? I'm here to help!"
                        
                        st.write("Debug - Response:", response)  # Debug info
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.write("Debug - Added assistant response to history")  # Debug info
                        
                        # Force a refresh to show the new messages
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ I encountered an error while searching: {str(e)}")
                        st.write("Debug - Error:", str(e))  # Debug info
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "I'm sorry, I ran into a problem. Could you please try asking again?"
                        })
                        st.rerun()  # Force a refresh to show the error message
            else:
                st.write("Debug - No user input provided")  # Debug info

if __name__ == "__main__":
    main() 