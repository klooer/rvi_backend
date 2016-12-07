"""
"""

from __future__ import absolute_import

import sys, os, logging, time, jsonrpclib, base64

from django.conf import settings


# Logging setup
logger = logging.getLogger('rvi')

# Globals
transaction_id = 0


def handle_control(vehicle, command):
    """
    Send control command to a vehicle
    :param vehicle:  Vehicle object
    :param command:  Control command
    """
    
    logger.info('Sending control command %s to %s.', command, vehicle)
    
    global transaction_id
    
    # get settings
    # service edge url
    try:
        rvi_service_url = settings.RVI_SERVICE_EDGE_URL
    except NameError:
        logger.error('RVI_SERVICE_EDGE_URL not defined. Check settings!')
        return False

    # get destination info
    dst_url = vehicle.veh_rvibasename + '/vin/' + vehicle.veh_vin
 
    # establish outgoing RVI service edge connection
    rvi_server = None
    logger.info('Establishing RVI service edge connection: %s', rvi_service_url)
    try:
        rvi_server = jsonrpclib.Server(rvi_service_url)
    except Exception as e:
        logger.error('Cannot connect to RVI service edge: %s', e)
        return False
    logger.info('Established connection to RVI Service Edge: %s', rvi_server)
    
    transaction_id += 1
    # send message
    rvi_server.message(service_name = dst_url + '/control',
                       transaction_id = str(transaction_id),
                       timeout = int(time.time()) + 60,
                       parameters = { u'command': command })
        
    logger.info('Sent control command.')
    
    # done
    return True

