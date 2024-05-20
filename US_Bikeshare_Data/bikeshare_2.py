import time
import pandas as pd
import numpy as np
import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

days= ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
months = ['january', 'february', 'march', 'april', 'may', 'june']
options = ['month', 'day', 'both', 'none']

def invalid_input():
    """
    Prints a message indicating invalid input.
    """
    print('-> Invalid input')

def get_user_input(prompt, options = []):
    """
    Prompts the user for input and validates it against a list of options (if provided).

    Args:
        (str) prompt : The message to display to the user requesting input
        (list[str]) options : A list of valid options the user can enter

    Returns:
        str: The user's input converted to lowercase and stripped of whitespace.
    """
    if not options:
        return input(prompt).lower().strip()
    else:
        # check input valid with same data
        while True:
            _input = input(prompt).lower().strip()
            if _input in options:
                return _input
            else:
                invalid_input()

def clear_console():
    """
    Clear the terminal 
    """
    os.system('cls')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*40)

    # while True:
    #     city = input('\nWould you like to see data for Chicago, New York, or Washington:\n').lower()
    #     if city in CITY_DATA:
    #         break
    #     else:
    #         invalid_input()
    
    # user input datasource and date
    city = get_user_input('\nWould you like to see data for Chicago, New York, or Washington:\n', CITY_DATA)

    while True:
        option = input('\nWould you like to filter the data by month, day, both, or not at all.\nType "none" for no time filter.\n').lower()
        if option in(options):
            break
        else:
            invalid_input()
    
    if option == 'month' or option == 'both':
        month = get_user_input("\nWhich month? " + ', '.join(months) +'\n', months)
    else:
        month = 'all'

    if option == 'day' or option == 'both':
        # check input valid
        # if number get day in original list
        while True:
            day = get_user_input('\nWhich day? Please enter your response as an integer or string:' + '\n' + ', '.join(days) + '\n(e.g., 1=Monday)' + '\n')
            if day in days:
                break
            elif day in ",".join(map(str, np.arange(1, 8))):
                day = days[int(day)]
                break
            else:
                invalid_input()

    else:
        day = 'all'

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
    
    f_name = CITY_DATA[city]

    # load data file into a dataframe
    df = pd.read_csv(f_name)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Add month column
    df['month'] = df['Start Time'].dt.month
    # Add day of week column
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        # create the new dataframe with index of month
        df = df[df['month'] == (months.index(month) + 1)]

    if day != 'all' :
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
        (DataFrame) df : A Pandas DataFrame containing trip data
    """

    print('\nPopular times of travel')
    start_time = time.time()

    # find the most common month and count occurrences
    common_month = df['month'].mode()[0]
    print("Most common month: %s, count: %d" % (months[common_month-1], df['month'].value_counts().iloc[0]))

    # find the most common day and count occurrences
    common_day = df['day_of_week'].mode()[0]
    print("Most common day: %s, count: %d" % (common_day, df['day_of_week'].value_counts().iloc[0]))

    # find the most popular hour and and count occurrences
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most popular start hour: %s, count: %d' % (common_hour, df['hour'].value_counts().iloc[0]))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Args:
        (DataFrame) df: A Pandas DataFrame containing trip data
    """

    print('\nPopular stations and trip')
    start_time = time.time()

    # display most commonly used start station and count occurrences
    common_start = df['Start Station'].mode()[0]
    print("Most common start station: %s, count: %d" % (common_start, df['Start Station'].value_counts().iloc[0]))

    # display most commonly used end station and count occurrences
    common_end = df['End Station'].mode()[0]
    print("Most common end station: %s, count: %d" % (common_end, df['End Station'].value_counts().iloc[0]))

    # display most frequent combination of start station and end station trip
    df['ste'] = df['Start Station'] + ' - ' + df['End Station']
    common_ste = df['ste'].mode()[0]
    print("Most common trip from start to end:",common_ste)

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Args:
        (DataFrame) df: A Pandas DataFrame containing trip data
    """

    print('\nTrip duration')
    start_time = time.time()

    # total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: %s, count: %d" % (total_travel_time, df['Trip Duration'].shape[0]))

    # average travel time
    average_travel_time = df['Trip Duration'].mean()
    print("Average travel time:", average_travel_time)

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Args:
        (DataFrame) df: A Pandas DataFrame containing trip data
    """

    print('\nUser info')
    start_time = time.time()

    print("\nCounts of each user type:")
    print(df['User Type'].value_counts())

    # check gender existed and count
    if 'Gender' in df:
        print("\nCounts of each gender:")
        print(df['Gender'].value_counts())

    # check birth year existed and calculator
    if 'Birth Year' in df:
        birth_info = {
            "Earliest": df['Birth Year'].min(),
            "Most Recent": df['Birth Year'].max(),
            "Most Common": df['Birth Year'].mode()[0]
        }
        # display key and value in loop
        for key, value in birth_info.items():
            print(f"\nThe {key} year of birth is: {value}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def load_more(df):
    """
    View a DataFrame in smaller chunks by prompting for confirmation after each chunk is displayed.

    Args:
        (DataFrame) df: The Pandas DataFrame containing the data to be loaded.

    Returns:
        Yields chunks of the DataFrame based on user input. It does not return a value.
    """

    # stores the initial total number of rows
    total = len(df.index)
    # limit row in new DataFrame
    limit = 5
    # start position
    offset = 0
    while total > 0:
        _input = input('=> Enter yes to continues: ').lower().strip()
        if _input == 'yes' or _input == 'y':
            # selects rows in the DataFrame df
            yield df.iloc[offset:offset + limit]
            offset += limit
            total -= limit
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # handle loading raw data 
        print("\nLoading data in chunks of 5 rows:")
        for chunk in load_more(df):
            print(chunk)

        restart = get_user_input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break

        clear_console()


if __name__ == "__main__":
	main()
