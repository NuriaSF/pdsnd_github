
import time
import statistics as stat
import sys
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
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    city=input('Please, introduce the name of the city you want to obtain information about [chicago/new york city/washington]: ')
    city=city.lower()
    #Let us now check that it is actually a valid input. We give 3 chances before exiting the program
    i=0
    while (city != 'chicago') and (city != 'new york city') and (city != 'washington'):
        city=input('That was not valid. Please, introduce a valid city [chicago/new york city/washington]: ')
        i += 1
        if i==3:
            sys.exit()

    # get user input for month (all, january, february, ... , june)
    ans_month=input('Do you want to filter by month? [y/n]: ')
    if ans_month=='n':
        month='all'
    elif ans_month=='y':
        month=input('Which month? [january/february/.../june]: ')
        month=month.lower()
        #we check that it is actually a valid input. We give 3 chances before exiting the program:
        i=0
        set_months=['january','february','march','april','may','june']
        while month not in set_months:
            month=input('That was not valid. Please, introduce a valid month [january/february/.../june]: ')
            i += 1
            if i==3:
                sys.exit()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    ans_day=input('Do you want to filter by day of week? [y/n]: ')
    if ans_day=='n':
        day='all'
    elif ans_day=='y':
        day=input('Which day? [monday/tuesday/.../sunday]: ')
        day=day.lower()
        #check that it is actually a valid input. We give 3 chances before exiting the program:
        i=0
        set_days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        while day not in set_days:
            day=input('That was not valid. Please, introduce a valid day [monday/tuesday/.../sunday]: ')
            i += 1
            if i==3:
                sys.exit()

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
    # load data file into a dataframe
    df=pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        num_month=1
        for mes in months:
            if mes==month:
                break
            else:
                num_month += 1

        # filter by month to create the new dataframe
        df = df[(df['month']) == num_month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[(df['day_of_week']) == day.title()]

    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        try:
            popular_month_num = stat.mode(df['month'])
            tot_months=['january','february','march','april','may','june']
            popular_month=tot_months[popular_month_num-1]
            print('The most common month is ',popular_month)
        except stat.StatisticsError:
            print('There is not a most frequent month')

    # display the most common day of week
    if day == 'all':
        try:
            popular_day = stat.mode(df['day_of_week'])
            print('The most common day of week is ',popular_day)
        except stat.StatisticsError:
            print('There is not a most frequent day')

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    try:
        popular_hour = stat.mode(df['hour'])
        print('The most common start hour is ',popular_hour)
    except stat.StatisticsError:
        print('There is not a most frequent hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        popular_start_station=stat.mode(df['Start Station'])
        print('The most common start station is ', popular_start_station)
    except stat.StatisticsError:
        print('There is not a most frequent start station')

    # display most commonly used end station
    try:
        popular_end_station=stat.mode(df['End Station'])
        print('The most common end station is ', popular_end_station)
    except stat.StatisticsError:
        print('There is not a most frequent end station')

    # display most frequent combination of start station and end station trip
    #We create a column that gives the combination of both stations.
    df['combination']=df['Start Station'] + ' / ' + df['End Station']
    try:
        popular_comb=stat.mode(df['combination'])
        print('The most common combination is ', popular_comb)
    except stat.StatisticsError:
        print('There is not a most frequent combination')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_time=df['Trip Duration'].sum()
    print('The total travel time is ', tot_time)

    # display mean travel time
    mean_time=df['Trip Duration'].mean()
    print('The mean travel time is ', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(' '*5 +'Counts of user types: ')
    print(df['User Type'].value_counts())


    if city != 'washington':
        # Display counts of gender
        # We set to 'Unknown' NaN values.
        if df['Gender'].isnull().sum() != 0:
            df['Gender'].fillna('Unknown', inplace=True)

        print('\n' + ' '*5 + 'Counts of user gender: ')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        # We first check that there is at least one non NaN in the 'Birth Year' column
        num_NaN=df['Birth Year'].isnull().sum()
        len_column=len(df['Birth Year'])
        if num_NaN == len_column:
            print('\nWe do not have any information about \'Birth Year\' for your chosen filter')
        else:
            print('\nThe earliest year of birth is ', df['Birth Year'].min())
            print('The most recent year of birth is ', df['Birth Year'].max())
            try:
                common_year=stat.mode(df['Birth Year'])
                print('The most common year of birth is ', common_year)
            except stat.StatisticsError:
                print('There is not a most common year of birth')

            # Give the number of unknowns with respect to the total (to see if the above information is representative)
            print('We had available {} number of \'Birth Years\' out of a total of {}'.format(len_column-num_NaN,len_column))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def main():
    '''
    This function asks the user to introduce the city, month and day of week about which they want some information.
    Then, it asks if such information is just the filtered data or some statistic information. If the former is chosen,
    the program shows the first 5 rows and asks the user if they want to see 5 more rows, and keeps asking until the user does
    not want to see more data. On the other hand, if the latter is chosen, then the user is asked which statistic they want to see.
    Moreover, this function checks whether the input introduced by the user is valid or not.
    '''
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #We ask to visualise all the data or just the statistics
        wish_vis=input('Do you want to see the data or the statistics? [data/statistics]: ' )

        #we check that it is actually a valid input. We give 3 chances before exiting the program:
        count_wish_vis=0
        while wish_vis not in ['data','statistics']:
            wish_vis=input('That was not valid. Please, introduce a valid input [data/statistics]: ')
            count_wish_vis += 1
            if count_wish_vis==3:
                sys.exit()

        if wish_vis == 'data':
            print(df.head())
            keep_showing=input('Do you want to see 5 more rows? [y/n]: ')

            #we check that it is actually a valid input. We give 3 chances before exiting the program:
            count_keep_showing=0
            while keep_showing not in ['y','n']:
                keep_showing=input('That was not valid. Please, introduce a valid input [y/n]: ')
                count_keep_showing += 1
                if count_keep_showing == 3:
                    sys.exit()

            #We keep asking whether to visualise more data or not
            count_keep_showing=2;
            while keep_showing == 'y':
                print(df.head(count_keep_showing*5))
                count_keep_showing += 1
                keep_showing=input('Do you want to see 5 more rows? [y/n]: ')


        if wish_vis == 'statistics':
            #We ask which statistics
            choice_stat=input('Which statistic do you want to see? [time,station,trip,user,all]. If you want more than one, write them separated by a blank space: ')
            choice_stat_list=choice_stat.split()

            error_count=0 #we will control if there is an error by means of this variable

            if 'time' in choice_stat_list:
                time_stats(df,month,day)
                error_count += 1
            if 'station' in choice_stat_list:
                station_stats(df)
                error_count += 1
            if 'trip' in choice_stat_list:
                trip_duration_stats(df)
                error_count += 1
            if 'user' in choice_stat_list:
                user_stats(df,city)
                error_count += 1
            if 'all' in choice_stat_list:
                time_stats(df,month,day)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df,city)
                error_count += 1

            #We detect if there is some invalid input. In such case, we exit the program.
            if error_count !=len(choice_stat_list):
                print('You have written some statistic option wrongly')
                sys.exit()

        restart = input('\nWould you like to restart? [y/n]:\n')
        if restart != 'y':
            break



if __name__ == "__main__":
	main()
