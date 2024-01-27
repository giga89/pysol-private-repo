"""Module to analyze transaction to pool"""
import logging
import sys
import math
import datetime
import time
from threading import Thread
from time import sleep

from user_class import User

from solana.rpc.api import Client
from spl.token.client import Token
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction

if __name__ == "__main__":             
    solana_client = Client("https://purple-purple-firefly.solana-mainnet.quiknode.pro/d10b73ab35fdb1bc20946f1d571007bfa47350af/")
    solana_client.get_largest_accounts().value[0].lamports