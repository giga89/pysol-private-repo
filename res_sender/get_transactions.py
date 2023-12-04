"""Module to analyze transaction to pool"""
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

def get_transaction(address):
    """Module to analyze transaction to pool"""
    solana_client = Client("https://purple-purple-firefly.solana-mainnet.quiknode.pro/d10b73ab35fdb1bc20946f1d571007bfa47350af/")
    pubkey = Pubkey.from_string(address)
    signatures=solana_client.get_signatures_for_address(pubkey, limit=100)
    for sing_sign in signatures.value:
        print(sing_sign.signature)
        trns = solana_client.get_transaction(sing_sign.signature)
        print(trns)
    
if __name__ == "__main__":
    get_transaction("2Dr1iVSAAZAZwnTahBBU3w97k6C8e8t3RiY428ycv5zG")