'''
TapInfluence CSV Uploader
Created: 7/6/2016
Python Version 2.7.11

This Script processes a CSV file and creates invoices
'''

import sys, csv, logging, recurly
from logging.handlers import RotatingFileHandler

# name of csv file to be passed as argument
csv_file = sys.argv[1]
log_level_desired = sys.argv[2]
testing_mode = (sys.argv[3] == 'True')

# recurly specific stuff
recurly.SUBDOMAIN = 'YOUR-SUBDOMAIN'
recurly.API_KEY = 'abcdef01234567890abcdef01234567890'

# Set a default currency for your API requests
recurly.DEFAULT_CURRENCY = 'USD'

def authenticate():
    logger.info('Attempting to Authenticate')
    # recurly specific stuff
    recurly.SUBDOMAIN = 'https://justdate.recurly.com'
    recurly.API_KEY = '70c38822639f49f1a17e167eb8876682'

    # Set a default currency for your API requests
    recurly.DEFAULT_CURRENCY = 'USD'

def process_csv(csv_to_process = csv_file, testing_mode = testing_mode):
    '''A function that Processes the CSV file passsed as an argument using
        a DictReader'''

    logger.info('Beginning to Process CSV: %s' % csv_to_process)
    logger.debug('Testing Mode: ' + str(testing_mode))
    # get the number of rows first
    file = open(csv_to_process)
    # subtract 1 for the header of column names
    row_count = len(file.readlines()) - 1
    logger.info('CSV file opened has %d rows to process.' % row_count)

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
                # TODO Deprecrate this once charges are successfully applied
                current_invoice.append(row)
                # save the row to the previous_row variable to be used next
                previous_row = row
                logger.debug('Saving current row to previous row.')

                # apply the charge to the account
                logger.debug('Attempting to Add charge: ' + str(testing_mode))
                add_adjustment(row, testing_mode)

            else:
                ''' if the invoice group of the current row is the same as the
                    invoice group of the previous row then add to the current
                    invoice'''
                if row['invoicegroup'] == previous_row['invoicegroup']:
                    if (index + 1) == row_count:
                        '''eof reached. just post the invoice'''
                        logger.info('Final Invoice Posted!')
                        # TODO post invoice
                    else:
                        '''not eof'''

                        # TODO deprecate this
                        current_invoice.append(row)

                        logger.info('Invoice Group is still the same, and '
                            'not EOF. Adding another charge to the current '
                            'invoice.')

                        # apply the charge to the account
                        add_adjustment(row, testing_mode)

                        logger.debug(('Index Count: {}').format(str(index)))
                        logger.debug('Saving current row to previous row.')
                        previous_row = row

                else:
                    ''' if the invoice group is different then just post the
                        invoice'''
                    # TODO Post Invoice
                    logger.info(('The Invoice Program has changed. A new '
                        'invoice of group {} has posted.').format(
                            previous_row['invoicegroup']))

                    # empty the current invoice to start fresh
                    # deprecate this once adjustment function is done
                    logger.debug('Dumping the current invoice. Starting a '
                        'fresh one.')
                    del current_invoice[:]

                    # then add the new row to a freshly emptied invoice
                    # TODO Deprecate this
                    current_invoice.append(row)

                    # apply the charge to the account
                    add_adjustment(row, testing_mode)

                    print 'A new Invoice has been created'

                    if (index + 1) == row_count:
                        ''' Eof reached. Just post the invoice'''
                        # TODO post invoice
                        logger.info('No remaining charges, Final invoice '
                            'posted')

                        # possibly add this to log file
                        # print current_invoice
                    else:
                        ''' It's not the eof and there's more adjustments to
                            add'''
                        print ('Not Eof. Continuing adding adjustments to new '
                            'invoice')
                        print current_invoice
                        previous_row = row

def retrieve_account(account_code):
    try:
      account = Account.get(account_code)
      return account
    except NotFoundError:
      logger.warning(('Account Not Found: {}').format(row['customername']))
      return False

def add_adjustment(charge, testing):
    ''' a function that adds charges to accounts'''
    print type(testing)
    if testing == False:
        logger.debug('BOOM')
        charge = Adjustment(
          description = charge['programname'],
          unit_amount_in_cents = (charge['amountdue'] * 100),
          currency = 'USD',
          quantity = 1,
          accounting_code = None,
          tax_exempt = False)
          # start_date = start_date
          # end_date = end_date
        account.charge(charge)

    else:
        logger.debug('Testing mode: True, do nothing.')

    logger.info(('Adding charge to: {} {} {} {} {} {} '
        'Invoice Group: {}').format(
        charge['influencerfirstname'],
        charge['influencerlastname'],
        charge['customername'],
        charge['programname'],
        charge['amountdue'],
        charge['postedat'],
        charge['invoicegroup']))

def post_invoice(account, terms_and_conditions = None, customer_notes = None,
    collection_method = 'automatic', net_terms = 30, po_number = None):
    ''' a function that posts the invoice with all charges on account '''

    # invoice() takes invoice attributes as optional kwargs
    invoice = account.invoice(
        terms_and_conditions = terms_and_conditions,
        customer_notes = customer_notes,
        collection_method = collection_method,
        net_terms = net_terms,
        po_number = po_number)

def initiate_logging(log_level = log_level_desired):
    global logger

    # set format of log entries
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s '
        '%(lineno)d: %(message)s')

    ''' get logger and set level designated by user. this is for printing to
        file only'''
    logger = logging.getLogger('TapInfluence.CSVUploader')
    logger.setLevel(str.upper(log_level))

    # set name of log file, set to multiple files instead
    #file_handler = logging.FileHandler('example.log')
    file_handler = RotatingFileHandler('log_file.log', mode = 'a',
        maxBytes = 5*1024*1024, backupCount = 2, encoding = None, delay = 0)

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
    logger.info('***** Starting New Upload ***** %s \n' % csv_file)
    authenticate()
    process_csv()
