#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 - Assignment 1 Part 2"""


import urllib2
import argparse
import logging
import logging.handlers
import datetime
import csv
import sys

class DownloadError(Exception):
    """ Object raises error"""
    pass

class IdNotFoundWarning(Exception):
    """ Object raises error"""
    pass


def main():
    """Main function that runs at start of program.

    Args:
        --url (string): command line parameter of url

    Returns:
        User promted to enters info. Program will search and return value.
        Outputs to error.log file

    Examples:
        >>> $ python assignment2.py --url  "http://website.com/birthdays100.csv"
        >>> Please enter an ID to look up: 1
        Person #1 is Charles Paige with a birthday of 1963-01-06 00:00:00
    """
    # Enable command-line arguments
    parser = argparse.ArgumentParser()
    # Add command-line argmuemnt --url that recives url string
    parser.add_argument('--url')
    args = parser.parse_args()

    # Set up logger named assignment2 with output level
    my_logger = logging.getLogger('assignment2')
    my_logger.setLevel(logging.WARNING)
    # Add the log message handler to the logger. output to file
    handler = logging.FileHandler('errors.log')
    my_logger.addHandler(handler)

    # Assgined data from url to csvData. Catch download errors and exit
    # If statement to handle >>> python -i file.py without --url
    if (args.url):
        try:
            csvData = downloadData(args.url)
        except DownloadError as exception:
            print "Error: {}. Program closing.".format(exception.message)
            my_logger.error('Error Download: {}'.format(exception.message))
            sys.exit()
    else:
        my_logger.error('Missing command-line argument. --url')
        sys.exit()

    # Process url data into dictionary with tuple values. Catch errors and exit
    try:
        personData = processData(my_logger,csvData)
    except IndexError as exception:
        my_logger.error(exception.message)
        print('Unable to read file. Program closing.')
        sys.exit()

    # Prompt user to input and return value from dictionaty.
    # Handle incorrect input like non-numbers (spec char and letters)
    # Exit when user enters 0 or neg nums
    while True:
        try:
            user_input = int(input("Please enter an ID to look up: "))
        except (SyntaxError, NameError) as exception:
            # what about floats?
            my_logger.error('Error: {}'.format(exception.message))
            print('You have not entered a number.')
            continue
        else:
            # int num entered. break loop and continue
            break

    if user_input > 0:
        try:
            displayPerson(user_input,personData)
        except IdNotFoundWarning as exception:
            my_logger.error(exception.message)
            main()

    else:
        print('Your selection means you want to leave. Goodbye')
        # exit program


def downloadData(url):
    """Download file from url

    Args:
        url (string): Url string

    Returns:
        Returns value of file
        Raise exceptions

    Examples:
        >>> $ python -i assignment2.py
        >>> downloadData('url.com/file.csv')
        This is the output of the file
    """
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        raise DownloadError(e.code)
    except urllib2.URLError as e:
        raise DownloadError(e.reason)

    return response


def processData(logger, data_to_process):
    """Process data from URL into dictionary that maps a person’s ID to a tuple
    of the form (name, birthday)

    Args:
        logger (unknown): Logging function
        data_to_process (string): string of data from url

    Returns:
        Returns dictionary
        Raise exceptions

    Examples:
        >>> $ python -i assignment2.py
        >>> processData(logger, string_data)
        {1:('Name',datetime object)}
    """
    new_dict = {}
    count = 1
    reader = csv.reader(data_to_process)

    for row in reader:
        if (count > 1): # skip the first row headers
            try:
                d = datetime.datetime.strptime(row[2], '%d/%m/%Y')
            except IndexError as exception:
                raise IndexError('Error processing line #{} for ID # Unknown.{}'
                                 .format(count,exception.message))
                break

            except ValueError:
                logger.error('Error processing line #{} for ID #{}'.format(count
                                                                       ,row[0]))
            else:
                new_dict[int(row[0])] = (row[1],d)

        count += 1

    return new_dict


def displayPerson(id,dict):
    """Displays process data from arguments

    Args:
        id (int): User ID to search
        dict (dictionary): string of data from url

    Returns:
        Returns dictionary
        Raise exceptions

    Examples:
        >>> $ python -i assignment2.py
        >>> displayPerson(id, dict)
        Person #1 is Charles Paige with a birthday of 1963-01-06 00:00:00
    """
    if id in dict:
        print 'Person #{} is {} with a birthday of {}'.format(id, dict[id][0],
                                                             dict[id][1])
    else:
        print 'Person #{} not found'.format(id)
        raise IdNotFoundWarning('Warning: Person#{} not found.'.format(id))


# Run main if file direcrly executed
if __name__ == '__main__':
    main()
