import pandas as pd
import re

data = pd.read_csv("../data/NYPL-menus.csv")
# print(data.head())

'''Select a subset of the data for cleaning with Python'''
subset = data[['event', 'venue', 'place', 'date']]
# print(subset.head())

'''Destructure DataFrame to return individual column Series to pass to functions'''
(event, venue, place, date) = subset['event'], subset['venue'], subset['place'], subset['date']

'''Functions to operate on each column and return cleaned data'''
def clean_event(event):
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

    return cleaned_event

def clean_venue(venue):
    venue = venue.str.replace(';', '')

    venue = venue.str.replace('?', '')

    venue = venue.str.replace('[', '', regex=True)
    venue = venue.str.replace(']', '', regex=True)

    cleaned_venue = venue.str.replace('\(\)', '', regex=True)

    cleaned_venue.to_csv("../data/test_venue.csv")

    return cleaned_venue

def clean_place(place):
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

    return cleaned_place

def clean_date(date):
    
    # Use a list comprehension to filter bad values and create a new Pandas Series
    cleaned_date = pd.Series([d for d in date if d != '0190-03-06' and d != '1091-01-27' and d != '2928-03-26'])
    
    cleaned_date.to_csv("../data/test_date.csv")

    return cleaned_date


'''Merge Pandas Series to DataFrame and output as CSV'''
def merge_series_to_df(cleaned_event, cleaned_venue, cleaned_place, cleaned_date):

    all_series = {"cleaned_event": cleaned_event, "cleaned_venue": cleaned_venue, "cleaned_place": cleaned_place, "cleaned_date": cleaned_date}
    
    df = pd.concat(all_series, axis=1)

    return df.to_csv("../data/cleaned-NYPL-menus.csv")


def main():

    cleaned_event = clean_event(event)

    cleaned_venue = clean_venue(venue)

    cleaned_place = clean_place(place)

    cleaned_date = clean_date(date)

    merge_series_to_df(cleaned_event, cleaned_venue, cleaned_place, cleaned_date)

if __name__ == "__main__":
    main()
