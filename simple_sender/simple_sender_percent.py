"""Module providing a function to open file"""
import logging
import sys
import math
import os
from user_class_2 import User

from solana.rpc.api import Client
from spl.token.client import Token
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction

from common import send_transaction_and_test
from common import get_quantity
from common import remove_space_and_n

#one element for each resource
users_array = []
quantity_res = 0
token_to_send = 0

program_id = Pubkey.from_string(
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
)
    
def add_quantity_to_user_in_array(user1, quantity):
    """Function add points to user"""
    for person in users_array:
        if person.addr == user1.addr:
            person.quantity = person.quantity + quantity
            return
    user1.quantity = quantity
    users_array.append(user1)

if __name__ == "__main__":

    logging.basicConfig(filename="log_simple_sender_percent.txt", level=logging.DEBUG)
    logger = logging.getLogger('')
    # create console handler and set level to debug
    ch = logging.FileHandler(filename="log_simple_sender_percent.txt", mode="a")
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    
    #privkey of sender
    privKey_arg = sys.argv[1]
    #address of sender
    source_arg = sys.argv[2]
    #send for real
    realSend = sys.argv[3]
    #index to start
    index_to_start = sys.argv[4]
    #index to start
    token_to_send = sys.argv[5]
    #file da leggere
    file=sys.argv[6]
    
    quantity_res = get_quantity(source_arg, privKey_arg, token_to_send)

    #populate array of user from files
    try:
        with open(file, "r", encoding="utf-8") as f:
            file_content = f.read()
            rows = file_content.split(';')
            for row in rows:
                elements_in_row = row.split(',')
                if len(elements_in_row) == 3:
                    #get all data from row user,address,quantity of resource
                    name=remove_space_and_n(elements_in_row[0])
                    wallet=remove_space_and_n(elements_in_row[1])
                    quantity=int((float(quantity_res)/100) * float(elements_in_row[2]))
                    u = User(name, wallet)
                    add_quantity_to_user_in_array(u,quantity)
    except IOError:
        logger.error("file: %s not found", "files/address.txt")

    INDEX=0
    INDEX_TRXS=0
    for user in users_array:
        if INDEX_TRXS > int(index_to_start):
            if realSend == "send":
                logger.debug("TRNS %d %s to %s IDX:[%d]",user.quantity, token_to_send, user.addr, INDEX_TRXS)
            else:
                logger.debug("FAKE TRNS %d %s to %s IDX:[%d]",user.quantity, token_to_send, user.addr, INDEX_TRXS)
            result = False
            while result == False:
                result = send_transaction_and_test(user.addr, token_to_send, user.quantity, privKey_arg, source_arg, logger, INDEX_TRXS)
        INDEX_TRXS+=1
    INDEX+=1
        
        