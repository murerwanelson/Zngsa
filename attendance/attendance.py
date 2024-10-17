# attendance.py
import pandas as pd

def process_attendance(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Clean the Data: Drop unnecessary columns
    columns_to_drop = ['Department', 'No.', 'Location ID', 'ID Number', 'VerifyCode', 'CardNo']
    df = df.drop(columns=columns_to_drop)
    
    # Extract Date and Time
    df['Date'] = pd.to_datetime(df['Date/Time']).dt.date  # Convert 'Date/Time' to Date
    df['Time'] = pd.to_datetime(df['Date/Time']).dt.time  # Convert 'Date/Time' to Time
    df = df.drop(columns=['Date/Time'])  # Drop original 'Date/Time' column
    
    # Group by Name and Date to get the first (min) and last (max) time for each person per day
    time_in_out = df.groupby(['Name', 'Date'])['Time'].agg(['min', 'max']).reset_index()
    time_in_out = time_in_out.rename(columns={'min': 'Time In', 'max': 'Time Out'})
    
    # Get unique names and unique dates from the data
    unique_names = df['Name'].unique()  # Unique names
    unique_dates = df['Date'].unique()  # Unique dates (from the original dataset)
    
    # Generate full attendance list using only the unique dates from the original data
    all_attendance = [{'Name': name, 'Date': date} for name in unique_names for date in unique_dates]
    all_attendance_df = pd.DataFrame(all_attendance)  # Create DataFrame for full attendance
    
    # Merge the full attendance with the time_in_out data to fill in attendance records
    attendance_df = pd.merge(all_attendance_df, time_in_out, on=['Name', 'Date'], how='left')
    
    # Mark attendance as 'Absent' by default
    attendance_df['Attendance'] = 'Absent'
    
    # Update attendance as 'Present' where there is a valid 'Time In' (i.e., not NaN)
    attendance_df.loc[attendance_df['Time In'].notnull(), 'Attendance'] = 'Present'
    
    # Return the final attendance DataFrame
    return attendance_df


# attendance.py function for processing data

"""def process_attendance(file_path):
    df = pd.read_csv(file_path)
    columns_to_drop = ['Department', 'No.', 'Location ID', 'ID Number', 'VerifyCode', 'CardNo']
    df = df.drop(columns=columns_to_drop)
    df['Date'] = pd.to_datetime(df['Date/Time']).dt.date
    df['Time'] = pd.to_datetime(df['Date/Time']).dt.time
    df = df.drop(columns=['Date/Time'])
    time_in_out = df.groupby(['Name', 'Date'])['Time'].agg(['min', 'max'])
    time_in_out = time_in_out.rename(columns={'min': 'Time In', 'max': 'Time Out'}).reset_index()

    unique_names = df['Name'].unique()
    date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max())

    all_attendance = [{'Name': name, 'Date': date.date()} for name in unique_names for date in date_range]
    attendance_df = pd.DataFrame(all_attendance)
    attendance_df = pd.merge(attendance_df, time_in_out, on=['Name', 'Date'], how='left')
    attendance_df['Attendance'] = attendance_df['Time In'].notnull().map({True: 'Present', False: 'Absent'})
    
    return attendance_df"""
