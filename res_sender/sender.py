"""Module providing a function to open file"""
import sys
import math

from user_class import User

#one element for each resource
users_array = []

# Python3 code to remove whitespace
def remove_space_and_n(string):
    """Function remove space and n char from a string"""
    result =  string.replace(" ", "")
    result =  result.replace("\n", "")
    return result

def add_point_to_user_in_array(user1, points):
    """Function add points to user"""
    for person in users_array:
        if person.name == user1.name:
            person.points = person.points + points
            return
    user1.points = points
    users_array.append(user1)

if __name__ == "__main__":

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
            print("file: " + resource + ".txt" + "not found")

    #print user and points of each user
    for user in users_array:
        print(user.name + "points: " + str(user.points) + "\r")

    #print total of each res
    INDEX=0
    for res in res_array_total:
        print(res_arr_str[INDEX] + " " +str(res))
        INDEX+=1

    INDEX=0
    for resource in res_arr_str:
        TOTAL = 0
        for user in users_array:
            QTD = res_array_total[INDEX]

            if QTD>0:
                RES_VAL = res_arr_val[INDEX]
                QFTR = math.floor((user.points / len(res_arr_val))/RES_VAL)
                TOTAL += QFTR
                print(user.name + " have to " + str(QFTR) + " of " + str(res_arr_str[INDEX]))

        print("total quantity of " + res_arr_str[INDEX] + " distribuited is " + str(TOTAL))
        INDEX+=1
        