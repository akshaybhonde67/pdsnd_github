import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, mth, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) mth - name of the mth to filter by, or "all" to apply no mth filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    invalid_inputs = "Invalid input. Please try again" 
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user raw_input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True :
        city = raw_input("\nenter the name of the city to analyze city names are as follows\nchicago,\nnew york,\nwashington. \n").lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print(invalid_inputs)
    
    # TO DO: get user raw_input for mth (all, january, february, ... , june)
    while True :
        mth = raw_input("\nenter the name of the mth\njanuary,\nfebruary,\nmarch,"
            "\napril,\nmay,\njune\nto filter by, or \"all\" to apply no mth filter\n").lower()
        if mth in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            print(invalid_inputs)

    # TO DO: get user raw_input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = raw_input("\nenter the name of the day\nmonday,\ntuesday,\nwednesday,\nthursday,"
            "\nfriday,\nsaturday,\nsunday\nof week to filter by, or \"all\" to apply no day filter\n").lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print(invalid_inputs)

    print('-'*40)
    return city, mth, day


def load_data(city, mth, day):
    """
    Loads data for the specified city and filters by mth and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) mth - name of the mth to filter by, or "all" to apply no mth filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by mth and day
    """
    file_name = CITY_DATA[city]
    print ("Accessing data from: " + file_name)
	#reading csv file
    df = pd.read_csv(file_name)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(arg = df['Start Time'], format = '%Y-%m-%d %H:%M:%S')

    # filter by mth if applicable
    if mth != 'all':
        # extract mth and day of week from Start Time to create new columns
        df['mth'] = df['Start Time'].dt.mth

        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        mth = months.index(mth) + 1

        # filter by mth to create the new dataframe
        df = df.loc[df['mth'] == mth]

    # filter by day of week if applicable
    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nMost Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert the Start Time column to datetime
	#convert to date time format of year-mth-day hrs-mins-secs
    df['Start Time'] = pd.to_datetime(arg = df['Start Time'], format = '%Y-%m-%d %H:%M:%S')

    # Create new columns for mth, weekday, hour
    mth = df['Start Time'].dt.mth
    weekday_name = df['Start Time'].dt.weekday_name
    hour = df['Start Time'].dt.hour
    
    # TO DO: display the most common mth
    most_common_month = mth.mode()[0]
    print('Most common mth: ', most_common_month)

    # TO DO: display the most common day of week
    most_common_day_of_week = weekday_name.mode()[0]
    print('Most common day of week: ', most_common_day_of_week)

    # TO DO: display the most common start hour
    common_start_hour = hour.mode()[0]
    print('Most frequent start hour: ', common_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nMost Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most commonly used start station:', df['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print('Most commonly used end station:', df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    combine_stations = df['Start Station'] + "*" + df['End Station']
    common_station = combine_stations.value_counts().idxmax()
    print('Most frequent used combinations are:\n{} \nto\n{}'.format(common_station.split('*')[0], common_station.split('*')[1]))

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # Convert seconds to readable time format
    def secs_to_readable_time(seconds):
        m, s = divmod(seconds,60)
        h, m = divmod(m,60)
        d, h = divmod(h,24)
        y, d = divmod(d,365)
        print('Years: {}, Days: {}, Hours: {}, Mins: {}, Secs: {}'.format(y,d,h,m,s))

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:\n')
    secs_to_readable_time(total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth: " + str(earliest_birth_year))
        print("\nMost recent year of birth: " + str(most_recent_birth_year))
        print("\nMost common year of birth: " + str(common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))    
    print('-'*40)

def raw_data(df):
    user_input = raw_input('Do you want to see raw data? Enter yes or no.\n')
    line_number = 0

    while 1 :
        if user_input.lower() != 'no':
            print(df.iloc[line_number : line_number + 5])
            line_number += 5
            user_input = raw_input('\nDo you want to see more raw data? Enter yes or no.\n')
        else:
            break    

def main():
    while 1 :
        city, mth, day = get_filters()
        df = load_data(city, mth, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = raw_input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()