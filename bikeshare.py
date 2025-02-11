import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city
    while True:
        city = input("Enter the city (chicago, new york city, washington):\n").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("Invalid city. Please try again.")

    # get user input for month (all, january, february, ... , june)
    valid_months = ['january','february','march','april','may','june','all']
    while True:
        month = input("Enter the month (january-june) or 'all':\n").lower()
        if month in valid_months:
            break
        else:
            print("Invalid month. Please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    while True:
        day = input("Enter the day of the week (monday-sunday) or 'all':\n").lower()
        if day in valid_days:
            break
        else:
            print("Invalid day. Please try again.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january','february','march','april','may','june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    print("Most Common Month (1=Jan ... 6=June):", most_common_month)

    most_common_day = df['day_of_week'].mode()[0]
    print("Most Common Day of Week:", most_common_day)

    most_common_hour = df['hour'].mode()[0]
    print("Most Common Start Hour:", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station:", start_station)

    end_station = df['End Station'].mode()[0]
    print("Most Common End Station:", end_station)

    df['combination'] = df['Start Station'] + " to " + df['End Station']
    most_common_combination = df['combination'].mode()[0]
    print("Most Common Trip:", most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    print("Total Travel Time:", round(total_time, 2), "seconds")

    mean_time = df['Trip Duration'].mean()
    print("Mean Travel Time:", round(mean_time, 2), "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print("Counts of User Types:\n", user_types)

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:\n", gender_counts)

    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest Year of Birth:", earliest)
        print("Most Recent Year of Birth:", recent)
        print("Most Common Year of Birth:", common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays 5 rows of data at a time upon user request."""
    i = 0
    pd.set_option('display.max_columns', 200)
    raw = input("Would you like to see 5 rows of raw data? Enter yes or no: ").lower()

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:i+5])
            i += 5
            raw = input("Would you like to see 5 more rows of data? Enter yes or no: ").lower()
        else:
            raw = input("\nInvalid input. Please enter only 'yes' or 'no': ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Call the new raw-data function here
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
