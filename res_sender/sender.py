import sys
import time
import numpy as np

from user_class import user

from solana.rpc.api import Client
from spl.token.client import Token
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction

#one element for each resource
users_array = []

def empty_user_array():
    print("delete all users")

def add_point_to_user_in_array(user, point_to_add):
    print("Handling user " + user.name)
    for person in users_array:
        if person['name'] == user.name:
            user.point = point_to_add
            print("Total point " + user.point)
            return person
    user.point = point_to_add
    users_array.add(user)
            
if __name__ == "__main__":

    #resources
    res_arr_str = ["arco", "biomass","carbon","copperOre","diamond","ironOre","lumanite","rochinol"] 
    res_arr_val = [100, 10, 10, 15, 100, 20, 40, 100] #random numbers waiting fonta/tori
    res_arr_address = ["ARCoQ9dndpg6wE2rRexzfwgJR3NoWWhpcww3xQcQLukg", 
                    "MASS9GqtJz6ABisAxcUn3FeR4phMqH1XfG6LPKJePog",
                    "CARBWKWvxEuMcq3MqCxYfi7UoFVpL9c4rsQS99tw6i4X",
                    "CUore1tNkiubxSwDEtLc3Ybs1xfWLs8uGjyydUYZ25xc",
                    "DMNDKqygEN3WXKVrAD4ofkYBc4CKNRhFUbXP4VK7a944",
                    "FeorejFjRRAfusN9Fg3WjEZ1dRCf74o6xwT5vDt3R34J",
                    "LUMACqD5LaKjs1AeuJYToybasTXoYQ7YkxJEc4jowNj",
                    "RCH1Zhg4zcSSQK8rw2s6rDMVsgBEWa4kiv1oLFndrN5"] 

    #privkey of sender
    privKey_arg = sys.argv[1]
    #address of sender
    source_arg = sys.argv[2]

    #populate array of user from files
    for resource in res_arr_str:
        f = open(resource + ".txt", "r")
        file_content = f.read()
        rows = file_content.split('\n')
        elements_in_row = file_content.split(',')
        #get all data from row user,address,quantity of resource
        u = user(elements_in_row[0], elements_in_row[1])
        #point depends to value of each resource
        point_to_add=elements_in_row[2]*res_arr_val[res_arr_str.index("resource")]
        add_point_to_user_in_array(u,point_to_add)
        f.close()

    #print user and points of each user
    for user in users_array:
        print(user.name + "points: " + user.point + "\r\n")