import pandas as pd
import re

    # @BEGIN main

def main():

    # @Param data @URI file: data/NYPL-menus.csv
    # @Param subset
    data = pd.read_csv("../data/NYPL-menus.csv")
    # print(data.head())

    '''Select a subset of the data for cleaning with Python'''
    subset = data[['event', 'venue', 'place', 'date']]
    # print(subset.head())

    '''Destructure DataFrame to return individual column Series to pass to functions'''
    (event, venue, place, date) = subset['event'], subset['venue'], subset['place'], subset['date']

    '''Functions to operate on each column and return cleaned data'''

    # @BEGIN cleaned_event
    # @IN event @as Event 
    # Work on this to remove all quotes
    event = event.str.replace('"', '', regex=True)
    event = event.str.replace('""', '', regex=True)
    event = event.str.lstrip('"')
    event = event.str.rstrip('"')


    event = event.str.replace('[', '', regex=True)
    event = event.str.replace(']', '', regex=True)

    # Match this: (?)
    pattern1 = '\(\?\)'
    event = event.str.replace(pattern1, '', regex=True)

    # Match semicolons at the end of the string
    pattern2 = '\;$'
    event = event.str.replace(pattern2, '', regex=True)

    # Match semicolons in the middle of a string and replace with :
    pattern3 = '\\b;'
    cleaned_event = event.str.replace(pattern3, ':', regex=True)

    cleaned_event.to_csv("../data/test_event.csv")

    # @OUT cleaned_event @as Cleaned_event
    # @END clean_event 

    # @BEGIN clean_venue 
    # @IN venue @as Venue
    venue = venue.str.replace(';', '')

    venue = venue.str.replace('?', '')

    venue = venue.str.replace('[', '', regex=True)
    venue = venue.str.replace(']', '', regex=True)

    cleaned_venue = venue.str.replace('\(\)', '', regex=True)

    cleaned_venue.to_csv("../data/test_venue.csv")

    # @OUT cleaned_venue @as Cleaned_venue
    # @END clean_venue

    # @BEGIN clean_place
    # @IN place @as Place
    place = place.str.replace('"', '', regex=True)
    place = place.str.replace('""', '', regex=True)
    place = place.str.lstrip('"')
    place = place.str.rstrip('"')

    place = place.str.replace(';', '')

    place = place.str.replace('?', '')

    place = place.str.replace('[', '', regex=True)
    place = place.str.replace(']', '', regex=True)

    place = place.str.replace('\(', '', regex=True)
    cleaned_place = place.str.replace('\)', '', regex=True)

    cleaned_place.to_csv("../data/test_place.csv")

    # @OUT cleaned_place @as Cleaned_place
    # @END clean_place    

    # @BEGIN clean_date
    # @IN date @as Date
    
    # Use a list comprehension to filter bad values and create a new Pandas Series
    cleaned_date = pd.Series([d for d in date if d != '0190-03-06' and d != '1091-01-27' and d != '2928-03-26'])
    
    cleaned_date.to_csv("../data/test_date.csv")

    # @OUT cleaned_date @As Cleaned_date
    # @END clean_date

    '''Merge Pandas Series to DataFrame and output as CSV'''
    # @BEGIN merge_series_to_df
    # @IN cleaned_event @As Cleaned_event
    # @In cleaned_venue @As Cleaned_venue
    # @In cleaned_place @As Cleaned_Place
    # @In cleaned_date @As Cleaned_date
    all_series = {"cleaned_event": cleaned_event, "cleaned_venue": cleaned_venue, "cleaned_place": cleaned_place, "cleaned_date": cleaned_date}

    df = pd.concat(all_series, axis=1)

    df.to_csv("../data/cleaned-NYPL-menus.csv")
    # @OUT df @As Cleaned_DataFrame
    # @END merge_series_to_df

# @END main

main()
