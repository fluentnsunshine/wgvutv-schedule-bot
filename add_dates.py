import pandas as pd
from datetime import datetime, timedelta

def add_dates_to_schedule():
    try:
        # Read the existing Excel file
        df = pd.read_excel('sample_tv_schedule.xlsx')
        
        # Get today's date
        today = datetime.now().date()
        
        # Create a list of dates (next 7 days)
        dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        
        # Create a new DataFrame with repeated schedule for each date
        new_rows = []
        for date in dates:
            for _, row in df.iterrows():
                if pd.notna(row['Program Title']):  # Only include rows with program titles
                    new_row = row.copy()
                    new_row['Date'] = date
                    new_rows.append(new_row)
        
        # Create new DataFrame with all rows
        new_df = pd.DataFrame(new_rows)
        
        # Save to a new Excel file
        new_df.to_excel('sample_tv_schedule_with_dates.xlsx', index=False)
        print("Successfully created 'sample_tv_schedule_with_dates.xlsx' with dates added!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    add_dates_to_schedule() 