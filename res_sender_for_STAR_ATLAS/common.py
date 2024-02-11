"""Module providing a function to open file"""
import logging
import sys
import math
import time

from solana.rpc.api import Client
from spl.token.client import Token
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction

program_id = Pubkey.from_string(
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
)

rpc_url = "https://mainnet.helius-rpc.com/?api-key=6297c3ea-594e-4fb1-a545-f132c3f838c7"


def send_transaction2(dest_address,res_address, res_quantity, privkey, source, logger):
    """ Send transaction on solana"""
    
    logger.debug("Send trns key:%s source:%s mint:%s dest:%s",privkey, source, res_address, dest_address)
    key_pair = Keypair.from_base58_string(privkey)
    source = Pubkey.from_string(source)
    mint = Pubkey.from_string(res_address)
    dest = Pubkey.from_string(dest_address)


    logger.debug("Send trns.")
    
    amount = res_quantity
    solana_client = Client(rpc_url)
    spl_client = Token(
        conn=solana_client, pubkey=mint, program_id=program_id, payer=key_pair
    )
    
    logger.debug("Send trns..")

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
        
    
    logger.debug("Send trns...")
        
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
    
    logger.debug("Send trns....")


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
    
    return transaction.value

def send_transaction_and_test(dest_address,res_address, res_quantity, privkey, source, logger, INDEX_TRXS):
    
    present_quantity = 0
    after_quantity = 0
    trns_done = 0
    while present_quantity == 0:
        try:
            present_quantity = get_quantity(source,privkey,res_address)
            logger.debug("[%d]quantity before %s", INDEX_TRXS, present_quantity)
        except: 
            logger.debug("[%d]quantity before check error", INDEX_TRXS)
            
    while trns_done == 0:
        try:
            logger.debug("Star send.. IDX:[%d]", INDEX_TRXS)
            trx = send_transaction2(dest_address, res_address, res_quantity, privkey, source, logger)
            trns_done = 1
            logger.debug("DONE IDX:[%d] https://solscan.io/tx/%s", INDEX_TRXS, trx)
        except: 
            print
            trns_done = 0
            logger.debug("RETRY IDX:[%d]", INDEX_TRXS)

    retry = 0
    while (after_quantity == present_quantity or after_quantity == 0) and retry < 50:
        try:
            after_quantity = get_quantity(source,privkey,res_address)
            logger.debug("[%d]quantity after %s", INDEX_TRXS, after_quantity)
            retry = retry + 1
        except: 
            logger.debug("[%d]quantity after check error", INDEX_TRXS)
        time.sleep(1)

            
            
    logger.debug("[%d]quantity difference %d",INDEX_TRXS , int(present_quantity) - int(after_quantity))
    
    if(int(present_quantity) - int(after_quantity) == res_quantity):
        logger.debug("Tutto ok")
        return True
    else:
        logger.debug("Qualcosa è andato male %d-%d!=%d",int(present_quantity),int(after_quantity),res_quantity)
        return False    
                                    

def get_quantity(source,privkey,mint):
    """ Send transaction on solana"""
    
    mint_pubkey = Pubkey.from_string(mint)
    source_pubkey = Pubkey.from_string(source)
    key_pair = Keypair.from_base58_string(privkey)

    solana_client = Client(rpc_url)
    spl_client = Token(conn=solana_client, pubkey=mint_pubkey, program_id=program_id, payer=key_pair)
    quantity_local = 0
        
    account = spl_client.get_accounts_by_owner(owner=source_pubkey)
        
    quantity_local = spl_client.get_balance(pubkey=account.value[0].pubkey)
    
    return quantity_local.value.amount

        

# Python3 code to remove whitespace
def remove_space_and_n(string):
    """Function remove space and n char from a string"""
    result =  string.replace(" ", "")
    result =  result.replace("\n", "")
    return result
