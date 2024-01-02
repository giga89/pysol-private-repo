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

#one element for each resource
users_array = []


program_id = Pubkey.from_string(
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
)

def send_transaction(dest_address,res_address, res_quantity, privkey, source):
    """ Send transaction on solana"""
    key_pair = Keypair.from_base58_string(privkey)
    source = Pubkey.from_string(source)
    mint = Pubkey.from_string(res_address)
    dest = Pubkey.from_string(dest_address)

    amount = res_quantity
    solana_client = Client("https://indulgent-small-grass.solana-mainnet.quiknode.pro/98eace00260cbb6d63ad1b34a222511a4cf79e3d/")
    spl_client = Token(
        conn=solana_client, pubkey=mint, program_id=program_id, payer=key_pair
    )

    try:
        source_token_account = (
            spl_client.get_accounts_by_owner(
                owner=source, commitment=None, encoding="base64"
            )
            .value[0]
            .pubkey
        )
        
    except:
        source_token_account = spl_client.create_associated_token_account(
            owner=source, skip_confirmation=False, recent_blockhash=None
        )
        
    try:
        dest_token_account = (
            spl_client.get_accounts_by_owner(owner=dest, commitment=None, encoding="base64")
            .value[0]
            .pubkey
        )
        
    except:
        dest_token_account = spl_client.create_associated_token_account(
            owner=dest, skip_confirmation=False, recent_blockhash=None
        )


    txn = Transaction()

    transaction = spl_client.transfer(
        source=source_token_account,
        dest=dest_token_account,
        owner=key_pair,
        amount=int(float(amount)),
        multi_signers=None,
        opts=None,
        recent_blockhash=None,
    )

    print(transaction)
    print(txn)

# Python3 code to remove whitespace
def remove_space_and_n(string):
    """Function remove space and n char from a string"""
    result =  string.replace(" ", "")
    result =  result.replace("\n", "")
    return result

def add_quantity_to_user_in_array(user1, quantity):
    """Function add points to user"""
    for person in users_array:
        if person.addr == user1.addr:
            person.quantity = person.quantity + quantity
            return
    user1.quantity = quantity
    users_array.append(user1)

if __name__ == "__main__":

    logging.basicConfig(filename="log_simple_sender.txt", level=logging.DEBUG)

    # create logger
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.FileHandler(filename="log.txt", mode="a")
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

    #populate array of user from files
    try:
        with open("files/address.txt", "r", encoding="utf-8") as f:
            file_content = f.read()
            rows = file_content.split(';')
            for row in rows:
                elements_in_row = row.split(',')
                if len(elements_in_row) == 3:
                    #get all data from row user,address,quantity of resource
                    name=remove_space_and_n(elements_in_row[0])
                    wallet=remove_space_and_n(elements_in_row[1])
                    quantity=int(remove_space_and_n(elements_in_row[2]))
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
                trns_done = 0
                while trns_done == 0:
                    try:
                        send_transaction(user.addr, token_to_send, user.quantity, privKey_arg, source_arg)
                        trns_done = 1
                        logger.debug("DONE IDX:[%d]", INDEX_TRXS)
                    except: 
                        print
                        trns_done = 0
                        logger.debug("RETRY IDX:[%d]", INDEX_TRXS)
            else:
                logger.debug("FAKE TRNS %d %s to %s IDX:[%d]",user.quantity, token_to_send, user.addr, INDEX_TRXS)
        INDEX_TRXS+=1
    INDEX+=1
        