import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Please enter the city in which you\'d like to explore the bikeshare data: ')
    city = str(input()).lower()
    while not (city in ['chicago','new york city','washington']):
        print('Sorry, that was an invalid input. Please try again: ')
        city = str(input()).lower()

    # get user input for month (all, january, february, ... , june)
    print('Now please enter the month which you\'d like to use as a filter for your data (use \'all\' if you want all the months): ')
    month = str(input()).lower()
    while not (month in ['all','january','february','march','april','may','june']):
        print('Sorry, that was an invalid input. Please try again: ')
        month = str(input()).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Now please enter the day of the week which you\'d like to use as a filter for your data (use \'all\' if you want all the days of the week): ')
    day = str(input()).lower()
    while not (day in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']):
        print('Sorry, that was an invalid input. Please try again: ')
        day = str(input()).lower()


    print('*'*10 + 'Great! you have chosen your desired city and the filters!' + '*'*10)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month: ' + months[most_common_month - 1].title())

    # display the most common day of week
    most_common_day_of_the_week = df['day_of_week'].mode()[0]
    print('The most common day of the week: ' + most_common_day_of_the_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common start hour: ' + str(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: ' + most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station is: ' + most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['Journeys'] = df['Start Station'].str.cat(df['End Station'], sep = ' to ')
    popular_journey = df['Journeys'].mode()[0]
    print('The most common trip taken is ' + popular_journey)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ' + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: ' + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types are as follows: ')
    print(user_types)
    print()

    # Display counts of gender (if the city is NYC or Chicago)
    if 'Gender' in df.columns: 
        gender_counts = df['Gender'].value_counts()
        print('The counts of gender are as follows: ')
        print(gender_counts)
        print()

    # Display earliest, most recent, and most common year of birth (if the city is NYC or Chicago)
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print('The earliest, most recent, and the most common year of birth are {}, {} and {} respectively'.format(earliest_birth,most_recent_birth,most_common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
