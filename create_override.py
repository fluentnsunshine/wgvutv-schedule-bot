import pandas as pd
from datetime import datetime, timedelta

def create_sample_override():
    # Get today's date
    today = datetime.now().date()
    
    # Create sample override data
    override_data = {
        'Program Title': [
            'Special: American Experience Marathon',
            'Breaking News Coverage',
            'PBS Kids Special: Arthur Marathon',
            'Local Documentary: Grand Rapids History',
            'Special: Nature Documentary'
        ],
        'Channel Name': [
            'WGVU',
            'WGVU',
            'WGVU',
            'WGVU',
            'WGVU'
        ],
        'Start Time': [
            '2:00 PM',
            '5:00 PM',
            '8:00 AM',
            '7:00 PM',
            '9:00 PM'
        ],
        'End Time': [
            '6:00 PM',
            '7:00 PM',
            '12:00 PM',
            '8:00 PM',
            '10:00 PM'
        ],
        'Date': [
            today + timedelta(days=1),  # Tomorrow
            today,                      # Today
            today + timedelta(days=2),  # Day after tomorrow
            today + timedelta(days=3),  # 3 days from now
            today + timedelta(days=1)   # Tomorrow
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(override_data)
    
    # Save to Excel
    df.to_excel('schedule_override.xlsx', index=False)
    print("✅ Created sample schedule_override.xlsx with special programming!")
    print("\nSample overrides include:")
    print("- Special American Experience Marathon")
    print("- Breaking News Coverage")
    print("- PBS Kids Special: Arthur Marathon")
    print("- Local Documentary")
    print("- Nature Documentary Special")

if __name__ == "__main__":
    create_sample_override() 