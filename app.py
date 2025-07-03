import streamlit as st
import pandas as pd
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="WGVU TV Schedule Bot",
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
    </style>
""", unsafe_allow_html=True)

def load_schedules():
    try:
        # Load both schedules
        override_df = pd.read_excel('schedule_override.xlsx')
        regular_df = pd.read_excel('sample_tv_schedule_with_dates.xlsx')
        return override_df, regular_df
    except FileNotFoundError as e:
        st.error(f"Error: Could not find schedule files. Please make sure both 'schedule_override.xlsx' and 'sample_tv_schedule_with_dates.xlsx' exist.")
        return None, None

def search_schedule(title, override_df, regular_df):
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

def main():
    # Header
    st.title("📺 WGVU TV Schedule Bot")
    st.markdown("""
        Find when your favorite shows are airing on WGVU! 
        Search for any show title and I'll tell you when it's on.
    """)
    
    # Load schedules
    override_df, regular_df = load_schedules()
    if override_df is None or regular_df is None:
        return
    
    # Search input
    user_input = st.text_input("🎯 What show are you looking for?", placeholder="Enter a show title...")
    
    if user_input:
        with st.spinner("Searching schedules..."):
            results, source = search_schedule(user_input, override_df, regular_df)
            
            if not results.empty:
                # Show results count and source
                st.markdown(f"**Found {len(results)} match(es) in the {source} schedule:**")
                
                # Create columns for better layout
                for _, row in results.iterrows():
                    with st.container():
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            # Format date and time
                            date = pd.to_datetime(row['Date']).strftime("%A, %B %d")
                            start = pd.to_datetime(str(row['Start Time'])).strftime("%I:%M %p")
                            end = pd.to_datetime(str(row['End Time'])).strftime("%I:%M %p")
                            
                            # Show show title and channel
                            st.markdown(f"📺 *{row['Program Title']}* on **{row['Channel Name']}**")
                            
                        with col2:
                            # Show date and time
                            st.markdown(f"🗓️ {date}")
                            st.markdown(f"⏰ {start} – {end}")
                        
                        st.markdown("---")
            else:
                st.warning("❌ No shows found matching your search.")
                st.info("💡 Try searching with a different title or check for typos.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center'>
            <p>Made with ❤️ for WGVU viewers</p>
            <p>Last updated: {}</p>
        </div>
    """.format(datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)

if __name__ == "__main__":
    main() 