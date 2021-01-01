#!/bin/python3

import matplotlib.pyplot as plt
from subprocess import check_output
from re import findall
from platform import system
import sys


# getting host name and ping amount
###################
try:
    host = sys.argv[1]             # users can pass host and pings
    amount_of_pings = sys.argv[2]  # from the command line
    print(amount_of_pings, host)   #

except IndexError:  # if user does not pass any arguments, python returns an index error
    print('[!] No arguments passed!')
    host = input('Enter server domain or service: ')  # ask user for host and ping amount
    amount_of_pings = input('Enter amount of pings: ')


print('[!] pinging', host, amount_of_pings, 'times.')


# getting the data
####################
command = 'ping -w 10 google.com'  # command defaults to bash

sys = system()  # platform.system() # system check

if sys == 'Linux':
    command = 'ping -w' + ' ' + str(amount_of_pings) + ' ' + str(host)  # command for bash
    print(command)

elif sys == 'Windows':
    command = 'ping /n' + ' ' + str(amount_of_pings) + ' ' + str(host)  # command for powershell

else:  # if the system is unknown, allow the user to enter their own command
    print('Unknown Platform!')
    choice = input('Would you like to enter your own command?')

    if choice == "yes":
        command = input('Enter command: ')
        print('[!] may not work as well..')
    else:
        print('¯\\_(ツ)_/¯')  # ¯\_(ツ)_/¯

try:
    output = check_output(command, shell=True)  # executing command to shell
except NameError:
    print('AN ERROR HAS OCCURRED!')
print('[!] pinging...')

# finding time taken to reach the server
############################################
output = str(output)  # from bytes-like to string for it to work with regex
ping = findall("time=[1234567890]+", output)  # regex to find the ms values

data = []  # list defined for later use


for string in ping:
    string = string.replace('time=', '')  # removing unused characters
    string = int(string)  # turning the number value to integer
    data.append(string)  # append result to another list

sorted(data, reverse=True)  # sorting values from smallest to biggest

# visualising data
#####################
amount_of_pings = int(amount_of_pings)
if len(data) != amount_of_pings:
    print("the server you pinged returned", len(data), ',when it should\'ve been', amount_of_pings)

print(amount_of_pings)
amount_of_pings = amount_of_pings + 1
plt.plot(data)  # plotting
plt.grid(axis='y', linestyle='-')  # lines for better
plt.grid(axis='x', linestyle='-')  # readability
plt.ylabel("Time taken to reach server in MS", fontsize=14)  # --------------------------- #
plt.xlabel('Pings', fontsize=14)                             # just some configurations ---#
plt.xticks(range(0, amount_of_pings, 2))                     # --------------------------- #
plt.show()
