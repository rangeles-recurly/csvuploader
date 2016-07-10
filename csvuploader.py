'''
TapInfluence CSV Uploader
Created: 7/6/2016
Python Version 2.7.11

This Script processes a CSV file and creates invoices
'''

import sys, csv, logging
from logging.handlers import RotatingFileHandler

# name of csv file to be passed as argument
csv_file = sys.argv[1]
log_level_desired = sys.argv[2]

api_key = 'blah'

def authenticate():
    print 'wow!'
    # TODO place authentication code here

def process_csv(csv_to_process = csv_file):
    '''A function that Processes the CSV file passsed as an argument using
        a DictReader'''

    logger.debug('We have a problem! OMG')

    # get the number of rows first
    file = open(csv_to_process)
    # subtract 1 for the header of column names
    row_count = len(file.readlines()) - 1
    print row_count

    # open the CSV
    with open(csv_to_process, mode = 'rb') as opened_csv:
        reader = csv.DictReader(opened_csv, restval = 'empty_column')

        # used to store the list of items in an invoice
        current_invoice = []

        # used as a marker for iterating
        previous_row = None

        for index, row in enumerate(reader):
            # TODO May need to add customer name or program name logic
            ''' use the invoice type first, then the program to add to a list
                and if it's the first record in the list'''
            if index == 0:
                # add the current dict to the current invoice being built
                current_invoice.append(row)
                # save the row to the previous_row variable to be used next
                previous_row = row
                print 'index: ' + str(index)
                '''elif index == total_rows - 1:
                    print 'last record, posting final invoice'
                    # TODO Post invoice
                    print 'Invoice Posted'
                    print current_invoice'''
            else:
                ''' if the invoice group of the current row is the same as the
                    invoice group of the previous row then add to the current
                    invoice'''
                if row['invoicegroup'] == previous_row['invoicegroup']:
                    if (index + 1) == row_count:
                        '''eof reached. just post the invoice'''
                        # TODO post invoice
                        print 'Final invoice posted!'
                    else:
                        '''not eof'''
                        current_invoice.append(row)
                        print ('Not eof adding another adjustment to the '
                               'current Invoice')
                        print 'index: ' + str(index)
                        previous_row = row

                else:
                    ''' if the invoice group is different then just post the
                        invoice'''
                    # TODO Post Invoice
                    print ('The invoice Program has changed. A new Invoice has '
                            'Posted')

                    # empty the current invoice to start fresh
                    del current_invoice[:]

                    # then add the new row to a freshly emptied invoice
                    current_invoice.append(row)
                    print 'A new Invoice has been created'

                    if (index + 1) == row_count:
                        ''' Eof reached. Just post the invoice'''
                        # TODO post invoice
                        print 'No remaining adjustments. Final invoice posted!'
                        print current_invoice
                    else:
                        ''' It's not the eof and there's more adjustments to
                            add'''
                        print ('Not Eof. Continuing adding adjustments to new '
                            'invoice')
                        print current_invoice
                        previous_row = row



def add_adjustment():
    # TODO place adjustment code here
    print 'wow!'

def post_invoice():
    # TODO place post Invoice code here
    print 'wow!'

def initiate_logging(log_level = log_level_desired):
    global logger

    # set format of log entries
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    ''' get logger and set level designated by user. this is for printing to
        file only'''
    logger = logging.getLogger('myapp')
    logger.setLevel(log_level)

    # set name of log file
    file_handler = logging.FileHandler('example.log')

    # this prints out to console
    console_handler = logging.StreamHandler(sys.stdout)

    # assign formatting to the handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the loggers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


if __name__ == "__main__":
    initiate_logging()
    process_csv()
