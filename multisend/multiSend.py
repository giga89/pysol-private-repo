import sys
import time

from solana.rpc.api import Client
from spl.token.client import Token
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction

privKey_arg = sys.argv[1]
source_arg = sys.argv[2]
file_address_arg = sys.argv[3]

f = open(file_address_arg, "r")

list_address_arg = f.read()

list_address_splitted = list_address_arg.split('\n')

mint = Pubkey.from_string(
    "GigVfd8XiQSWjqkixbFpTEbh8nbfyYNVEkNZwj16947h"
) 
program_id = Pubkey.from_string(
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
) 

key_pair = Keypair.from_base58_string(privKey_arg)

solana_client = Client("https://purple-purple-firefly.solana-mainnet.quiknode.pro/d10b73ab35fdb1bc20946f1d571007bfa47350af/")
spl_client = Token(
    conn=solana_client, pubkey=mint, program_id=program_id, payer=key_pair
)

source = Pubkey.from_string(source_arg)

for x in list_address_splitted:
    print(x)
    row = x.split(',')
    print("We are ready to sent to next address: ")
    print(row[0])
    print("Quantity: ")
    print(row[1])

    dest = Pubkey.from_string(row[0])
    amount = row[1]
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

    time.sleep(1)
    
exit()

