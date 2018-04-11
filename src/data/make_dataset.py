# -*- coding: utf-8 -*-
import os
from fnmatch import fnmatch
import csv
import click
import logging
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('rawdata_dir', type=click.Path(exists=True))
@click.argument('processeddata_dir', type=click.Path())
def main(rawdata_dir, processeddata_dir):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
        If the names 'raw' and 'processed' are changed, go to Makefile
        to make those changes, not here.

        More specifically, english language tweets are extracted and
        added to one file
    """
    logger = logging.getLogger(__name__)
    logger.info("""
                process all raw data files and extract tweets
                in english based on metadata""")
    # obtain  list of files (csv data per day)
    list_files = os.listdir(rawdata_dir)
    pattern = '*.csv'
    list_files = [file for file in list_files if fnmatch(file, pattern)]
    day_of_month =  lambda x: int(x[:2])
    month_of_year = lambda x: int(x[3:5])
    list_files.sort(key=day_of_month)
    list_files.sort(key=month_of_year)
    column_dict = {'lang':12,
                   'text':4,
                   'id':0,
                   'created_at':2}
    keys = ["id","created_at","text"]
    #filter english tweets and save them to processeddata_dir
    with open(os.path.join(processeddata_dir,'tweets.csv'),'w') as processed_data:
      firstfile = True
      for file in list_files:
        neng = 0
        ntot = 0
        #headerline is present in every file
        # skip the header for all filesexcept the first
        ifheader=True
        with open(os.path.join(rawdata_dir,file),'r') as raw_data:
          csv_reader = csv.reader(raw_data)
          for row in csv_reader:
            ntot += 1
            if ifheader:
              if firstfile:
                print(",".join([row[column_dict[key]] for key in keys]),
                      file=processed_data)
              else:
                ifheader=False
                continue
            else:
              if row[column_dict['lang']][:2]=='en':
                neng += 1
                print(",".join([row[column_dict[key]] for key in keys]),
                      file=processed_data)
          if (firstfile):
            firstfile=False
        logger.info("""{} --> found {} english tweets out of {} ({:0.2f}%)""".format(file,neng,ntot,neng*100.0/ntot))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
