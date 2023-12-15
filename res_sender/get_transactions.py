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

total_count=0

def get_transaction(address,sig_before = 0):
    global total_count
    #if sig_before:    
    INDEX=0
    """Module to analyze transaction to pool"""
    solana_client = Client("https://purple-purple-firefly.solana-mainnet.quiknode.pro/d10b73ab35fdb1bc20946f1d571007bfa47350af/")
    pubkey = Pubkey.from_string(address)
    found = False
    transaction_get = 0
    while transaction_get == 0:
        try:
            #print(pubkey)
            if sig_before == 0:
                signatures=solana_client.get_signatures_for_address(pubkey, commitment="finalized")
                print("trns found: " + str(len(signatures.value)))
                transaction_get = 1
            else:
                print("Saerch from..") 
                print(str(sig_before)) 
                signatures=solana_client.get_signatures_for_address(pubkey, commitment="finalized", before=sig_before)
                transaction_get = 1
        except:
            sleep(1)
            print("RETRY..")
            
    print("trns found: " + str(len(signatures.value)))
    for sing_sign in signatures.value:
        last_sign = sing_sign.signature
        if not found:
            transaction_get = 0
            transaction = 0
            while transaction_get == 0:
                try:
                    print("#[" + str(INDEX) + "," + str(total_count) + "] of:" + str(pubkey) + "signature: " + str(sing_sign.signature))                        
                    transaction = solana_client.get_transaction(sing_sign.signature)
                    transaction_get = 1
                except:
                    print("Ignore error..")
                    transaction_get = 2

            INDEX=INDEX+1
            total_count=total_count+1
            
            if transaction_get == 1:
                receiver = 0
                mint = 0
                sender = 0
                token_sender_post = 0
                token_receiver_post = 0
                token_sender_pre = 0
                token_receiver_pre = 0

                
                try:
                    sender = transaction.value.transaction.transaction.message.account_keys[0]
                    print("sender: " + str(sender))
                    receiver = 0
                                            
                    if len(transaction.value.transaction.meta.pre_token_balances) != 0:
                        mint = transaction.value.transaction.meta.pre_token_balances[0].mint
                        print("mint: " + str(mint))
                
                    if len(transaction.value.transaction.meta.pre_token_balances) != 0:
                        if (transaction.value.transaction.meta.pre_token_balances[0].owner == sender):
                            token_sender_pre = transaction.value.transaction.meta.pre_token_balances[0].ui_token_amount.amount
                        else:
                            receiver = transaction.value.transaction.meta.pre_token_balances[0].owner
                            token_receiver_pre = transaction.value.transaction.meta.pre_token_balances[0].ui_token_amount.amount
                
                    if len(transaction.value.transaction.meta.pre_token_balances) >1 :
                        if (transaction.value.transaction.meta.pre_token_balances[1].owner == sender):
                            token_sender_pre = transaction.value.transaction.meta.pre_token_balances[1].ui_token_amount.amount
                        else:
                            receiver = transaction.value.transaction.meta.pre_token_balances[1].owner
                            token_receiver_pre = transaction.value.transaction.meta.pre_token_balances[1].ui_token_amount.amount

                    if len(transaction.value.transaction.meta.post_token_balances) != 0:
                        if (transaction.value.transaction.meta.post_token_balances[0].owner == sender):
                            token_sender_post = transaction.value.transaction.meta.post_token_balances[0].ui_token_amount.amount
                        if (transaction.value.transaction.meta.post_token_balances[0].owner == receiver):
                            token_receiver_post = transaction.value.transaction.meta.post_token_balances[0].ui_token_amount.amount
                
                    if len(transaction.value.transaction.meta.post_token_balances) >1 :
                        if (transaction.value.transaction.meta.post_token_balances[1].owner == sender):
                            token_sender_post = transaction.value.transaction.meta.post_token_balances[1].ui_token_amount.amount
                        if (transaction.value.transaction.meta.post_token_balances[1].owner == receiver):
                            token_receiver_post = transaction.value.transaction.meta.post_token_balances[1].ui_token_amount.amount
                

                    quantity = int(token_receiver_post) - int(token_receiver_pre)
                    
                    print(str(transaction.value.block_time))
                    dt = datetime.datetime.fromtimestamp(transaction.value.block_time)
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    print(formatted_time)
                    
                    if(time.time() - transaction.value.block_time > 259200):
                        print("too old. Bye")
                        found=True
                    
                    if(str(receiver) == "2Dr1iVSAAZAZwnTahBBU3w97k6C8e8t3RiY428ycv5zG"):
                        file1 = open(str(mint)+".txt", "a")  # append mode
                        file1.write("utente,")
                        file1.write(str(sender))
                        file1.write(",")
                        file1.write(str(quantity) + ";")
                        file1.write('\n')
                        file1.close()
                        found = True
                except:
                    print("Shit happens") 
    if not found:     
        get_transaction(address, last_sign)                  
            
    
if __name__ == "__main__":
            
    total_count=0
    with open("sender_wallets.txt", "r", encoding="utf-8") as f:
        file_content = f.read()
        rows = file_content.split('\n')
        for row in rows:
            print(row)
            INDEX=0 
            
        threads = [Thread(target=get_transaction, args=[row,0]) for row in rows]
    
        # start the threads
        for thread in threads:
            thread.start()

        # wait for the threads to complete
        for thread in threads:
            thread.join()