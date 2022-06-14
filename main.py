# 
#   INAC INDEX calculator based on a school fish model
# 
# Created by: Sebastian Pineda Ospina
#      email: sepinedaos@unal.edu.co
#         on: 05/05/2022
# 

import logging
from readDataBase import readINAC, readZoo, readDistances
from schoolFishModel import calculateIndex

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')



filenameINAC = './CSVs/INAC.csv'
filenameDistances = './CSVs/Distances.csv'

# Composition of database = ['Department', 'INAC [2019, 2020, 2020-Calculated]', 'zooDepartments', 'Distances']
database = readINAC(filenameINAC)
database = readZoo(database)
database = readDistances(database, filenameDistances)
logging.info('Database Created: ')
logging.info(database)

# Calculate INAC Index based on school fish model
database = calculateIndex(database)

for index in range(1, len(database), 1):
    # print('index: ', index)
    err = database[index][1][1] - database[index][1][2]
    print(database[index][0],';',database[index][1][0],';',database[index][1][1],';',database[index][1][2],';',err)
