import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    city_choice = ''
    while city_choice.lower() not in CITY_DATA:
        city_choice = input("Which city would you like bikeshare data on? Chicago, New York City or Washington?\n")
    if city_choice.lower() in CITY_DATA:
        city = CITY_DATA[city_choice.lower()]
    else:
        print("Sorry your response was invalid, please enter one of the selections as stated above.")

    # Get user input for month (all, january, february, ... , june).
    month_choice = ''
    while month_choice.lower() not in MONTH_DATA:
        month_choice = input(
            "Which month would you like data for? (Input your selection as January, February, March etc. or type all to combine each months data\n")
    if month_choice.lower() in MONTH_DATA:
        month = month_choice.lower()
    else:
        print("Sorry but your request was invalid please input a data request that adheres to the mentioned choices")

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    day_choice = ''
    while day_choice.lower() not in DAY_DATA:
        day_choice = input(
            "Which day would you like data for? (Input your selection as Monday, Tuesday, Wednesday etc... or type all to combine each days data\n")
    if day_choice.lower() in DAY_DATA:
        day = day_choice.lower()
    else:
        print("Sorry but your request was invalid, please input a data request that adheres to the mentioned choices")

    print('-' * 40)
    return city, month, day

    print('-' * 40)
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
    # Load data file into a dataframe.
    df = pd.read_csv(city)

    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable.
    if month != 'all':
        # Use the index of the months list to get the corresponding int.
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe.
        df = df[df['month'] == month]

    # Filter by day of week if applicable.
    if day != 'all':
        # Filter by day of week to create the new dataframe.
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Display the most common month and capitalize.
    common_month = df['month'].mode()[0]
    month_name = MONTH_DATA[common_month].title()
    print("The most common month from the data is: " + month_name)

    # Display the most common day of week.
    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of the week from the data is:" + common_day_of_week)

    # Display the most common start hour.

    common_start_hour = df['hour'].mode()[0]
    print("The most common start hour from the data is:" + str(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station from the data is:" + common_start_station)

    # Display most commonly used end station.
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station from the data is:" + common_end_station)

    # Display most frequent combination of start station and end station trip.
    common_station_combination = (df['Start Station'] + 'to' + df['End Station']).mode()[0]
    print("The most common combination of start and end stations are:" + str(common_station_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time and convert to readable time.
    total_travel_time = df['Trip Duration'].sum()
    hours, remainder = divmod(total_travel_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(
        "The total travel time from the data requested is: {} hours, {} minutes, and {} seconds.".format(hours, minutes,
                                                                                                         seconds))

    # Display mean travel time and convert to readable time.
    mean_travel_time = df['Trip Duration'].mean().round(1)
    minutes, seconds = divmod(mean_travel_time, 60)

    print("The mean travel time from the data requested is: {} minutes and {} seconds.".format(int(minutes),
                                                                                               int(seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_type_count = df['User Type'].value_counts()
    print("The count of user types from the requested data:\n" + str(user_type_count))

    # Display counts of gender.
    if 'Gender' in df.columns:
        gender_type_count = df['Gender'].value_counts()
        print("\nThe count of user gender from the requested data:\n" + str(gender_type_count))
    else:
        print("The 'Gender' column does not exist in the selected dataset.")

    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print("\nThe earliest birth year from the requested data: " + str(int(earliest_birth_year)))
        print("The most recent birth year from the requested data: " + str(int(recent_birth_year)))
        print("The most common birth year from the requested data: " + str(int(common_birth_year)))
    else:
        print("The 'Birth Year' column does not exist in the selected dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# Allow user to pull raw data, 5 rows at a time.

def display_raw_data(df):
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five rows of raw data? Please enter yes or no.\n')
        if view_raw_data.lower() == 'yes':
            print(df.iloc[next:next + 5])
            next = next + 5
        elif view_raw_data.lower() == 'no':
            return
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


# Allow user to loop back to start of program to pull new data or close program.

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        next_index = 0
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
