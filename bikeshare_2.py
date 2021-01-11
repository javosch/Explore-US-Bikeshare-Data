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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    instructions_city = 'Choose a city -->\n' +\
        '\nFor Chicaco press C' +\
            '\nFor New York press NY' +\
            '\nFor Washington press W' +\
                '\nFor all cities press ALL' +\
                    '\nIf you want to cancel press CTRL+C' +\
                        '\n\n'
    
    print(instructions_city)
    
    cities = {'C':'Chicago',
              'NY':'New York City',
              'W':'Washington',
              'ALL':'All cities'}
    
    city = ''
    
    while True:
        city = input().upper()
        if (city == 'C') or (city == 'NY') or (city == 'W') or (city == 'ALL'):
            break
        else:
            print('Enter a valid option or cancel with CTRL+C')
            continue
        
    print('\nYou choosed city was: {}'.format(cities.get(city)))
        
            

    # get user input for month (all, january, february, ... , june)
    instructions_month = 'Choose a month by his number -->\n' +\
        '\nFor january press 1' +\
            '\nFor february press 2' +\
                '\nFor march press 3' +\
                    '\nFor april press 4' +\
                        '\nFor may press 5' +\
                            '\nFor june press 6' +\
                                '\nFor all months availables press 7' +\
                                    '\nIf you want to cancel press CTRL+C' +\
                                        '\n\n'
    
    print(instructions_month)
    
    month_names = {1:'January',
                   2:'February',
                   3:'March',
                   4:'April',
                   5:'May',
                   6:'June',
                   7:'All months availables'}
    
    month = 0
    
    
    while True:
        try:
            month = int(input())
            if (month >= 1) and (month <= 7):
                break
            else:
                print('Enter a valid option or cancel with CTRL+C')
                continue 
        except ValueError:
            print('Only accept natural numbers between 1 and 6 inclusive.')
            continue
    
    print('\nYou choosed month was: {}'.format(month_names.get(month)))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    instructions_day = 'Choose a day by his number -->\n' +\
    '\nFor monday press 1' +\
        '\nFor tuesday press 2' +\
            '\nFor wednesday press 3' +\
                '\nFor thrusday press 4' +\
                    '\nFor friday press 5' +\
                        '\nFor saturday press 6' +\
                            '\nFor sunday press 7' +\
                                '\nFor select all days press 8\n' +\
                                    '\nIf you want to cancel press CTRL+C' +\
                                        '\n\n'
    
    print(instructions_day)
    
    days_names = {1:'Monday',
                  2:'Tuesday',
                  3:'Wednesday',
                  4:'Thursday',
                   5:'Friday',
                   6:'Saturday',
                   7:'Sunday',
                   8:'All days'}

    day = 0
    
    while True:
        try:
            day = int(input())
            if (day >= 1) and (day <= 8):
                break
            else:
                print('Enter a valid option or cancel with CTRL+C')
                continue
        except ValueError:
            print('Only accept natural numbers between 1 and 8 inclusive.')
            continue

    print('\nYour day is: {}.'.format(days_names.get(day)))
    

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
    
    #Washington data have 8 columns not 10 like others. Gender and Birth Year left.
    
    c_path = 'chicago.csv'
    ny_path = 'new_york_city.csv'
    w_path = 'washington.csv'
    
    c_data = pd.read_csv(c_path)
    ny_data = pd.read_csv(ny_path)
    w_data = pd.read_csv(w_path)
    
    c_data['city'] = pd.Series(['C' for i in range(len(c_data.index))])
    ny_data['city'] = pd.Series(['NY' for i in range(len(ny_data.index))])
    w_data['city'] = pd.Series(['W' for i in range(len(w_data.index))])
    
    data = [c_data, ny_data, w_data]
    
    df = pd.concat(data)
    
    
    #Set Start Time and End Time as datetime column in pandas
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y%m%d %H:%M:%S')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y%m%d %H:%M:%S')
    
    #Get rid of july because there are only 40 values
    df = df[(df['End Time'].dt.month <= 6)]
    
    #Add columns for times
    df['Month Start'] = df['Start Time'].dt.month_name()
    df['Month End'] = df['End Time'].dt.month_name()
    df['Day Start'] = df['Start Time'].dt.day_name()
    df['Day End'] = df['End Time'].dt.day_name()
    df['Hour Start'] = df['Start Time'].dt.hour
    df['Hour End'] = df['End Time'].dt.hour
    df['Minute Start'] = df['Start Time'].dt.minute
    df['Minute End'] = df['End Time'].dt.minute
    
    
    #Get another DataFrame for answers with all data
    #df2 = df.copy(deep=True) #----> can't use without changing the variable
    #inputs in the other function

    
    if city == 'ALL':
        if (month <= 6) and (day <= 7):
            df = df[(df['End Time'].dt.month == month) &\
                    (df['End Time'].dt.dayofweek == day-1)]
        elif (month <= 6):
            df = df[(df['End Time'].dt.month == month)]
        elif (day <= 7):
            df = df[(df['End Time'].dt.dayofweek == day-1)]
        else:
            df
    else:
        if (month <= 6) and (day <= 7):
            df = df[(df['End Time'].dt.month == month) &\
                    (df['End Time'].dt.dayofweek == day-1) &\
                        (df['city'] == city)]
        elif (month <= 6):
            df = df[(df['End Time'].dt.month == month) &\
                    (df['city'] == city)]
        elif (day <= 7):
            df = df[(df['End Time'].dt.dayofweek == day-1) &\
                    (df['city'] == city)]
        else:
            df = df[df['city'] == city]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, originaly with df2 but changed to df.
    count_month = dict(df.groupby('Month End')['End Time'].count())
    max_month = df.groupby('Month End')['End Time'].count().max()
    common_month = [key for key, value in count_month.items() \
                    if value == max_month][0]
    
    
    print('The most common month is: {}. With {} uses.'\
          .format(common_month, max_month))
    
    # display the most common day of week
    count_day = dict(df.groupby('Day End')['End Time'].count())
    max_day = df.groupby('Day End')['End Time'].count().max()
    common_day = [key for key, value in count_day.items() \
                  if value == max_day][0]
    
    
    print('The most common day of the week is: {}. With {} uses.'\
          .format(common_day, max_day))

    # display the most common start hour
    count_hour = dict(df.groupby('Hour End')['End Time'].count())
    max_hour = df.groupby('Hour End')['End Time'].count().max()
    common_hour = [key for key, value in count_hour.items() \
                  if value == max_hour][0]
    
    
    print('The most common hour of the day is: {}:00. With {} uses.'\
          .format(common_hour, max_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    count_start_station = dict(df.groupby('Start Station')['Start Station'].count())
    max_start_station = df.groupby('Start Station')['Start Station'].count().max()
    common_start_station = [key for key, value in count_start_station.items() \
                  if value == max_start_station][0]
    
    
    print('The most common start station is: {}:. With {} uses.'\
          .format(common_start_station, max_start_station))


    # display most commonly used end station
    count_end_station = dict(df.groupby('End Station')['End Station'].count())
    max_end_station = df.groupby('End Station')['End Station'].count().max()
    common_end_station = [key for key, value in count_end_station.items() \
                  if value == max_end_station][0]
    
    
    print('The most common end station is: {}:. With {} uses.'\
          .format(common_end_station, max_end_station))

    # display most frequent combination of start station and end station trip
    df['com_start_end'] = 'Start Station: ' + df['Start Station'] + \
        ' and End Station: ' +  df['End Station']
    
    count_com_station = dict(df.groupby('com_start_end') ['com_start_end'].count())
    max_com_station = df.groupby('com_start_end') ['End Time'].count().max()
    common_com_station = [key for key, value in count_com_station.items() \
                  if value == max_com_station][0]
    
    
    print('The most common combination are {}:. With {} uses.'\
          .format(common_com_station, max_com_station))        


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip = df['Trip Duration'].sum()
    total_trip_hours = total_trip/60
    total_trip_days = total_trip_hours/24
    total_trip_years = total_trip_days/365
    
    print('Total Trips:\nMinutes: {}\nHours: {}\nDays: {}\nYears: {}'\
          .format(int(total_trip),
                  int(total_trip_hours),
                  int(total_trip_days),
                  int(total_trip_years)))

    # display mean travel time
    mean_trip = df['Trip Duration'].mean()
    mean_trip_hours = mean_trip/60
    
    print('\nMean Trip:\nMinutes: {}\nHours: {}'\
          .format(int(mean_trip),
                  int(mean_trip_hours)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df_users = df.dropna(subset=['User Type'], inplace=False)
    count_users = dict(df_users.groupby('User Type')['User Type'] .count())
    
    
    print('\nThere are {} types of users:'\
          .format(len(count_users)))
    
    for key, value in count_users.items():
        print('{}: {} users.'.format(key, value))

    # Display counts of gender
    types_gender = df.dropna(subset=['Gender'], inplace=False).nunique() 
    count_gender = dict(df.groupby('Gender')['Gender'].count())
    
    
    print('\nThere are {} types of gender:'\
          .format(len(count_gender)))
    
    for key, value in count_gender.items():
        print('{}: {} gender.'.format(key, value))

    # Display earliest, most recent, and most common year of birth
    earliest_birth = df.dropna(subset=['Birth Year'], inplace=False)['Birth Year']\
        .min()
    recent_birth = df.dropna(subset= ['Birth Year'],inplace=False)['Birth Year']\
        .max()
    
    count_birth = dict(df.groupby('Birth Year') ['Birth Year'].count())
    max_birth = df.groupby('Birth Year') ['Birth Year'].count().max()
    
    try:
        common_birth = [key for key, value in count_birth.items() \
                        if value == max_birth][0]
    
        print('\nEarliest year birth: {}'.format(int(earliest_birth)))
        print('Most recent year birth: {}'.format(int(recent_birth)))
        print('The most common year birth is {}: with {} users.'\
              .format(int(common_birth), max_birth))
    
    except IndexError:
        print("\nThere aren't any birth data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = input('Would you like to see 5 rows of data?').upper()
    start_loc = 0
    end_loc = 5
    
    while view_data == 'YES':
        start_loc += 5
        end_loc += 5
        print(df.iloc[start_loc:end_loc])
        view_data = input('Would you like to see another 5 rows of data? \n')\
            .upper()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
