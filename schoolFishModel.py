# 
#   School Fish Model
# 
# Created by: Sebastian Pineda Ospina
#      email: sepinedaos@unal.edu.co
#         on: 06/05/2022
# 

from asyncio.log import logger
from distutils.log import debug
import logging
from random import random

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')

# Calculated based on the max deviation in INAC indexes between 2019 and 2020
theta_max = 15.86
theta_min = -14.12

# Parameters required in the model based on literature
etha = 0
noise_amp = 0

nOfIterations = 50


def calculateIndex(database):

    # Dif matrix: [Department name, dif zoo calculated, zoo indexes, dif zoa calculated, r zoo max, dif total]
    dif = []
    for i in range(0, (len(database)-1)):
        aux = [database[i+1][0], 0, database[i+1][2], 0, 0, 0]
        dif.append(aux)
    logging.debug("Dif matrix created")
    logging.debug(dif)

    # First try, Narinio and Vichada as seeds
    # Narino's and Vichada's Indexes are used as a seed to feed the model, because this departments have the highest and lowest difference between 2019 and 2020 indexes
    feed_indx = [20, 31]
    for i in feed_indx:
        dif[i][5] = database[i+1][1][1] - database[i+1][1][0]
        logging.debug('%s Dif: %f', dif[i][0], dif[i][5])
    logging.debug('Seed implanted')

    # Second try, Amazonas and Guajira as seeds
    # feed_indx = [0, 15]
    # for i in feed_indx:
    #     dif[i][5] = database[i+1][1][1] - database[i+1][1][0]
    #     logging.debug('%s Dif: %f', dif[i][0], dif[i][5])
    # logging.debug('Seed implanted')

    # Third try, Sucre and Bolivar as seeds
    # feed_indx = [4, 27]
    # for i in feed_indx:
    #     dif[i][5] = database[i+1][1][1] - database[i+1][1][0]
    #     logging.debug('%s Dif: %f', dif[i][0], dif[i][5])
    # logging.debug('Seed implanted')

    # Fourth try, Vaupes and Choco as seeds
    # feed_indx = [11, 30]
    # for i in feed_indx:
    #     dif[i][5] = database[i+1][1][1] - database[i+1][1][0]
    #     logging.debug('%s Dif: %f', dif[i][0], dif[i][5])
    # logging.debug('Seed implanted')


    # Calculate r zoo max
    for i in range(0, len(dif)):
        rzoomax = 0

        for ii in range(0, len(dif[i][2])):
            aux1 = dif[i][2][ii]
            aux2 = database[i+1][3][aux1]
            if aux2 > rzoomax:
                rzoomax = aux2
        
        dif[i][4] = rzoomax
    logging.debug("r zoo max calculated")
    logging.debug(dif)


    # Calculate dif zoo, dif zoa and dif total with the seed
    for k in range(0, nOfIterations):
        
        # dif total
        for i in range(0, len(dif)):
            if i == feed_indx[0] or i == feed_indx[1]:  # seed's dif are set before
                pass
            else:
                dif[i][5] = dif[i][1] + dif[i][3]    # dif total = dif zoo + dif zoa

        # dif zoo
        for i in range(0, len(dif)):
            if i == feed_indx[0] or i == feed_indx[1]:
                pass
            else:
                aux = 0
                for j in range(0, len(dif[i][2])):
                    val = dif[dif[i][2][j]][5]
                    if val != 0:
                        aux += val
                dif[i][1] = aux
        
        # dif zoa
        if not (etha == 0 or etha == 1):
            logging.warning("Etha != 0  or Etha != 1 is not recomended")
        
        for i in range(0, len(dif)):
            aux1 = 0
            aux3 = 0

            if dif[i][4] != 0:
                for ii in range(0, len(dif)):
                    isZoo = False
                    isSame = False

                    for iii in range(0, len(dif[i][2])):
                        if ii == dif[i][2][iii]:
                            isZoo == True
                    
                    if i == ii:
                        isSame = True

                    if not (isZoo or isSame):
                        aux2 = dif[i][4] / database[i+1][3][ii]
                        if aux2 < 1:
                            aux3 += dif[ii][5] * aux2
                        else:
                            aux3 += dif[ii][5]
            
            dif[i][3] = etha * aux3

    logging.debug('Dif Matrix iterated')
    logging.debug(dif)


    # Noise values check
    if noise_amp >= 2:
        logging.warning("Using high noise values")


    # Set INAC values in database matrix
    for n in range(1, len(database)):

        if n == (feed_indx[0]+1) or n == (feed_indx[1]+1):
            database[n][1][2] = database[n][1][0] + dif[n-1][5]
        else:
            # Noise
            noise = round(noise_amp * (random()), 2)

            if dif[n-1][5] >= 0:
                if dif[n-1][1] >= theta_max:
                    database[n][1][2] = database[n][1][0] + theta_max + noise
                    logging.warning("Theta max used in %s", database[n][0])
                else:
                    database[n][1][2] = database[n][1][0] + dif[n-1][5] + noise
            else:
                if dif[n-1][5] <= theta_min:
                    database[n][1][2] = database[n][1][0] + theta_min + noise
                    logging.warning("Theta min used in %s", database[n][0])
                else:
                    database[n][1][2] = database[n][1][0] + dif[n-1][5] + noise

    return database
