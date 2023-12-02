"""Module providing a function to open file"""
import logging
import sys
import math

from user_class import User

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

def send_transaction(dest_address,res_address, res_quantity, privKey_arg, source_arg):
    """ Send transaction on solana"""
    key_pair = Keypair.from_base58_string(privKey_arg)
    source = Pubkey.from_string(source_arg)
    mint = Pubkey.from_string(res_address)
    dest = Pubkey.from_string(dest_address)

    amount = res_quantity
    solana_client = Client("https://purple-purple-firefly.solana-mainnet.quiknode.pro/d10b73ab35fdb1bc20946f1d571007bfa47350af/")
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

def add_point_to_user_in_array(user1, points):
    """Function add points to user"""
    for person in users_array:
        if person.addr == user1.addr:
            person.points = person.points + points
            return
    user1.points = points
    users_array.append(user1)

if __name__ == "__main__":

    logging.basicConfig(filename="log.txt", level=logging.DEBUG)

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

    #resources
    res_arr_str = ["arco","carbon","copperOre","diamond","ironOre","lumanite","rochinol"]
    res_arr_val = [446, 100, 142, 445, 136, 193, 450]
    res_arr_address = ["ARCoQ9dndpg6wE2rRexzfwgJR3NoWWhpcww3xQcQLukg",
                    "CARBWKWvxEuMcq3MqCxYfi7UoFVpL9c4rsQS99tw6i4X",
                    "CUore1tNkiubxSwDEtLc3Ybs1xfWLs8uGjyydUYZ25xc",
                    "DMNDKqygEN3WXKVrAD4ofkYBc4CKNRhFUbXP4VK7a944",
                    "FeorejFjRRAfusN9Fg3WjEZ1dRCf74o6xwT5vDt3R34J",
                    "LUMACqD5LaKjs1AeuJYToybasTXoYQ7YkxJEc4jowNj",
                    "RCH1Zhg4zcSSQK8rw2s6rDMVsgBEWa4kiv1oLFndrN5"] 
    res_array_total = [0, 0, 0, 0, 0, 0, 0]

    #privkey of sender
    privKey_arg = sys.argv[1]
    #address of sender
    source_arg = sys.argv[2]
    #send for real
    realSend = sys.argv[3]
    #index to start
    index_to_start = sys.argv[4]

    #populate array of user from files
    for resource in res_arr_str:
        try:
            with open("files/" + resource + ".txt", "r", encoding="utf-8") as f:
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
                        #point depends to value of each resource
                        point_to_add=quantity*int(res_arr_val[res_arr_str.index(resource)])
                        add_point_to_user_in_array(u,point_to_add)
                        #add res to total of this res
                        idx = res_arr_str.index(resource)
                        res_array_total[idx] = res_array_total[idx] + quantity
        except IOError:
            logger.error("file: %s.txt not found", resource)

    TOTAL_POINTS = 0
    #print user and points of each user
    for user in users_array:
        logger.debug("%s points: %d", user.addr, user.points)
        TOTAL_POINTS = TOTAL_POINTS + user.points

    for user in users_array:
        #x:100 = point:total
        user.percent = (100*user.points) / (TOTAL_POINTS)
        logger.debug("%s %f%%", user.name, user.percent)
    #print total of each res
    TAX=4
    INDEX=0
    for res in res_array_total:
        logger.debug("total %s %d", res_arr_str[INDEX], int(res))
        TAXES = (4 * res) /100
        res_array_total[INDEX] = res - TAXES
        logger.debug("taxes %s %d", res_arr_str[INDEX],int(TAXES))
        logger.info("net %s %d", res_arr_str[INDEX],res_array_total[INDEX])
        INDEX+=1

    INDEX=0
    INDEX_TRXS=0
    for resource in res_arr_str:
        TOTAL = 0
        for user in users_array:
            QTD = res_array_total[INDEX]
            if QTD>0:
                if INDEX_TRXS > int(index_to_start):
                    QFTR = math.floor((user.percent/100) * QTD)
                    TOTAL += QFTR

                    if realSend == "send":
                        logger.debug("TRNS %d %s to %s IDX:[%d]",QFTR, res_arr_address[INDEX], user.addr, INDEX_TRXS)
                        send_transaction(user.addr, res_arr_address[INDEX], QFTR, privKey_arg, source_arg)
                    else:
                        logger.debug("FAKE TRNS %d %s to %s IDX:[%d]",QFTR, res_arr_address[INDEX], user.addr, INDEX_TRXS)
                INDEX_TRXS+=1

        logger.info("%f %s distribuited",TOTAL, res_arr_str[INDEX])
        INDEX+=1
        