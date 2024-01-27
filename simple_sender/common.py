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
    solana_client = Client("https://mainnet.helius-rpc.com/?api-key=6297c3ea-594e-4fb1-a545-f132c3f838c7")
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
    
    return transaction.value

def get_quantity(source,privkey,mint):
    """ Send transaction on solana"""
    
    mint_pubkey = Pubkey.from_string(mint)
    source_pubkey = Pubkey.from_string(source)
    key_pair = Keypair.from_base58_string(privkey)

    solana_client = Client("https://purple-purple-firefly.solana-mainnet.quiknode.pro/d10b73ab35fdb1bc20946f1d571007bfa47350af/")
    spl_client = Token(conn=solana_client, pubkey=mint_pubkey, program_id=program_id, payer=key_pair)
    quantity_local = 0
        
    account = spl_client.get_accounts_by_owner(owner=source_pubkey)
    
    #print(account.value[0].pubkey)
    
    quantity_local = spl_client.get_balance(pubkey=account.value[0].pubkey)
    
    return quantity_local.value.amount

        

# Python3 code to remove whitespace
def remove_space_and_n(string):
    """Function remove space and n char from a string"""
    result =  string.replace(" ", "")
    result =  result.replace("\n", "")
    return result
