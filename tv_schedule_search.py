import pandas as pd
from datetime import datetime

def search_tv_schedule(show_title):
    try:
        # First try to read the override file
        try:
            override_df = pd.read_excel('schedule_override.xlsx')
            override_df = override_df.dropna(subset=['Program Title'])
            override_df['Program Title'] = override_df['Program Title'].fillna('').astype(str)
            
            # Search in override file
            override_matches = override_df[override_df['Program Title'].str.lower().str.contains(show_title, na=False, case=False)]
            
            if not override_matches.empty:
                print("\n🎯 Found in schedule overrides:")
                print("=" * 50)
                for _, row in override_matches.iterrows():
                    show_date = row['Date']
                    start_time = row['Start Time']
                    end_time = row['End Time']
                    
                    # Format date and time nicely
                    formatted_date = pd.to_datetime(show_date).strftime("%A, %B %d")
                    formatted_start = pd.to_datetime(str(start_time)).strftime("%I:%M %p")
                    formatted_end = pd.to_datetime(str(end_time)).strftime("%I:%M %p")
                    
                    print(f"📺 *{row['Program Title']}* airs on {row['Channel Name']} 📡")
                    print(f"🗓️  {formatted_date}")
                    print(f"⏰  {formatted_start} – {formatted_end}")
                    print("-" * 50)
                return
        except FileNotFoundError:
            # If override file doesn't exist, continue to regular schedule
            pass
        
        # If no override found, check regular schedule
        df = pd.read_excel('sample_tv_schedule_with_dates.xlsx')
        df = df.dropna(subset=['Program Title'])
        df['Program Title'] = df['Program Title'].fillna('').astype(str)
        
        matches = df[df['Program Title'].str.lower().str.contains(show_title, na=False, case=False)]
        
        if matches.empty:
            print(f"\n❌ Sorry, I couldn't find any shows matching '{show_title}'")
            return
        
        print(f"\n🎯 Found {len(matches)} airing(s) of shows matching '{show_title}':")
        print("=" * 50)
        
        for _, row in matches.iterrows():
            show_date = row['Date']
            start_time = row['Start Time']
            end_time = row['End Time']
            
            # Format date and time nicely
            formatted_date = pd.to_datetime(show_date).strftime("%A, %B %d")
            formatted_start = pd.to_datetime(str(start_time)).strftime("%I:%M %p")
            formatted_end = pd.to_datetime(str(end_time)).strftime("%I:%M %p")
            
            print(f"📺 *{row['Program Title']}* airs on {row['Channel Name']} 📡")
            print(f"🗓️  {formatted_date}")
            print(f"⏰  {formatted_start} – {formatted_end}")
            print("-" * 50)
            
    except FileNotFoundError:
        print("❌ Error: Required schedule files not found.")
        print("ℹ️  Please make sure 'sample_tv_schedule_with_dates.xlsx' exists.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

def main():
    print("📺 TV Schedule Search Bot 📺")
    print("=" * 30)
    print("Hi! I can help you find when your favorite shows are airing.")
    print("Just type in a show title and I'll tell you when it's on!")
    print("Type 'quit' when you're done.")
    print("-" * 30)
    
    while True:
        show_title = input("\n🎯 What show would you like to search for? ")
        
        if show_title.lower() == 'quit':
            print("\n👋 Thanks for using TV Schedule Search! Have a great day!")
            break
            
        if show_title.strip():
            search_tv_schedule(show_title)
        else:
            print("❌ Please enter a valid show title.")

if __name__ == "__main__":
    main() 