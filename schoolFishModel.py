# 
#   School Fish Model
# 
# Created by: Sebastian Pineda Ospina
#      email: sepinedaos@unal.edu.co
#         on: 06/05/2022
# 

from asyncio.log import logger
import logging
from random import random

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')

# Calculated based on the max deviation in INAC indexes between 2019 and 2020
theta_max = 15.86
theta_min = -14.12

# Parameters required in the model based on literature
etha = 0

def calculateIndex(database):

    # Dif matrix: [Department name, dif calculated, zoo indexes]
    dif = []
    for i in range(0, (len(database)-1)):
        aux = [database[i+1][0],0,database[i+1][2]]
        dif.append(aux)
    logging.debug("Dif matrix created")
    logging.debug(dif)

    # First try, Narinio and Vichada as seeds
    # Narino's and Vichada's Indexes are used as a seed to feed the model, because this departments have the highest and lowest difference between 2019 and 2020 indexes
    # feed_indx = [20, 31]
    # for i in feed_indx:
    #     dif[i][1] = database[i+1][1][1] - database[i+1][1][0]
    #     logging.debug('%s Dif: %f', dif[i][0], dif[i][1])
    # logging.debug('Seed implanted')

    # Second try, Amazonas and Guajira as seeds
    # feed_indx = [0, 15]
    # for i in feed_indx:
    #     dif[i][1] = database[i+1][1][1] - database[i+1][1][0]
    #     logging.debug('%s Dif: %f', dif[i][0], dif[i][1])
    # logging.debug('Seed implanted')

    # Third try, Sucre and Bolivar as seeds
    # feed_indx = [4, 27]
    # for i in feed_indx:
    #     dif[i][1] = database[i+1][1][1] - database[i+1][1][0]
    #     logging.debug('%s Dif: %f', dif[i][0], dif[i][1])
    # logging.debug('Seed implanted')

    # Fourth try, Vaupes and Choco as seeds
    feed_indx = [11, 30]
    for i in feed_indx:
        dif[i][1] = database[i+1][1][1] - database[i+1][1][0]
        logging.debug('%s Dif: %f', dif[i][0], dif[i][1])
    logging.debug('Seed implanted')

    # Calculate difs with the seed
    nOfIterations = 50
    for k in range(0, nOfIterations):
        for i in range(0, len(dif)):
            if i == feed_indx[0] or i == feed_indx[1]:
                pass
            else:
                aux = 0
                for j in range(0, len(dif[i][2])):
                    val = dif[dif[i][2][j]][1]
                    if val != 0:
                        aux += dif[dif[i][2][j]][1]
                if aux != 0:
                    # print(dif[i][0], ' val: ', aux / len(dif[i][2]))
                    dif[i][1] = aux
                else:
                    dif[i][1] = 0
    logging.debug('Dif Matrix iterated')
    logging.debug(dif)
        
    if etha != 0:
        logging.warning("Etha != 0 is not implemented")
        pass

    # Set INAC values in database matrix
    for n in range(1, len(database)):

        if n == (feed_indx[0]+1) or n == (feed_indx[1]+1):
            database[n][1][2] = database[n][1][0] + dif[n-1][1]
        else:
            # Noise
            noise_amp = 0.5
            noise = round(noise_amp * (random()), 2)

            if dif[n-1][1] >= 0:
                if dif[n-1][1] >= theta_max:
                    database[n][1][2] = database[n][1][0] + theta_max + noise
                else:
                    database[n][1][2] = database[n][1][0] + dif[n-1][1] + noise
            else:
                if dif[n-1][1] <= theta_min:
                    database[n][1][2] = database[n][1][0] + theta_min + noise
                else:
                    database[n][1][2] = database[n][1][0] + dif[n-1][1] + noise

    return database
