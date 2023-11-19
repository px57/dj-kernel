import os
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_title(message):
    """
        @description
    """
    if type(message) != str:
        message = str(message)
    print (bcolors.BOLD + bcolors.OKGREEN + message + bcolors.ENDC)


def run_cmd_after_print(cmd, exec=False):
    """
        @description: 
    """
    print (bcolors.BOLD + bcolors.OKGREEN + cmd + bcolors.ENDC)
    os.system(cmd)