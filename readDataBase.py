# 
#   Read From CSVs
# 
# Created by: Sebastian Pineda Ospina
#      email: sepinedaos@unal.edu.co
#         on: 05/05/2022
#

import csv
import logging
from zooDatabase import zooDatabase
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')

# Save the info given in the database
database = [['Department', 'INAC [2019, 2020, 2020-Calculated]', 'zooDepartments', 'Distances']]  # Add a header

def readINAC(inputFilename):
    with open(inputFilename, 'r') as rawData:
        reader_handle = csv.reader(rawData)

        logging.info('Reading INAC Indexes')
        for line in list(reader_handle):
            database.append([line[0], [float(line[1]),float(line[2]), 0], [], []])
        
        return database

def readZoo(database):
    logging.info('Reading zoo departments')
    for i in range(1,len(database)):
        database[i][2] = zooDatabase[i-1]
        logging.debug(database[i])
    return database

def readDistances(database, filenameDistances):
    logging.info('Reading distances')
    with open(filenameDistances, 'r') as rawData2:
        reader_handle2 = csv.reader(rawData2)

        logging.debug('Reading distances')
        aux2 = 0
        for line in list(reader_handle2):
            aux2 += 1
            numOfDepts = 32
            aux1 = []
            for j in range(0, numOfDepts):
                aux1.append(int(line[j+1]))
            database[aux2][3] = aux1
        
        return database
