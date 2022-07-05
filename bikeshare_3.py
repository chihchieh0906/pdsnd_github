# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 13:04:00 2022

@author: CJ
"""

import time
import pandas as pd
import numpy as np

    # Getting data from respective csv files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new_york_city': 'new_york_city.csv',
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
    city = input ('Would you like to see data for chicago, new_york_city, or washington?\n')
    city = city.lower()
    while city not in ['chicago', 'new_york_city', 'washington']:
            city = input('Sorry! The city entered was not correct. Please enter again (chicago, new_york_city, washington): ')
            city = city.lower()
           
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)

    filters = input("Filter by month or day or both?\n")
    filters = filters.lower()
    while filters not in ['month', 'day', 'both']:
        filters = input("month or day or both?")
        filters = filters.lower()

    if filters in ['both', 'month']:
        month = input("Which month? January, February, March, April, May, June? or 'All'\n")  
        month = month.title()
        while month not in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            month = input("Sorry! The month entered was not correct. Please enter again (January, February, March, April, May, June or 'all')")
            month = month.title()
    else:
        month = 'All'
    

    if filters in ['both', 'day']:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? or 'all'\n")
        day = day.title()
        while day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all']:
            day = input('Sorry! The day entered was not correct. Please enter again(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all)')
            day = day.title()
    else:
        day = 'All'

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
    
    df['month']=df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    if month != 'All':
        months = ['January', 'February', 'March','April', 'May', 'June']
        month = months.index(month)+1
        
        df = df[df['month'] == month]
        # day : Monday or Tuesday ....
        if day != 'All':
            # transfer string to number 
            day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day.title())
            df = df[df['day_of_week'] == day]
            
    return df.reset_index()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of week:', popular_day)
    
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour:', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station:', popular_start)
    
    # display most commonly used end station
    popular_end = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station:', popular_end)
    
    # display most frequent combination of start station and end station trip
    popular_combo = df[['Start Station', 'End Station']].value_counts().idxmax()
    print('The most frequent combination of start station and end station trip:', popular_combo)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total travel time:', total_duration)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('Mean travel time:', mean_duration)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    # Display counts of gender
    if 'Gender' in df.columns:
        df['Gender'].fillna(0)
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
    # else:
    #     print("Gender column not exists")
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        year_earliest = df['Birth Year'].min()
        year_common = df['Birth Year'].value_counts().idxmax()
        year_recent = df['Birth Year'].max()
        
        print('Earliest year of birth:', year_earliest)
        print('Most recent year of birth:', year_recent)    
        print('Most common year of birth:', year_common)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_rdata(df):
    """ Prompt the user if they want to see 5 lines of raw data"""
    
    count = 0
    
    while True:
        answer = input('\nDo you want to see 5 {}lines of raw data? yes or no\n'.format('' if count == 0 else 'more '))
        if answer != 'yes' and answer != 'no':
            continue
        if answer == 'no':
            break
        print(df.loc[count:count+4])
        count +=5
        if count > df.shape[0]:
            break
        
        
        
    
    print('-'*40)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_rdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()