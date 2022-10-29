"""
Title: Computer Settings Bot
Date Started: Oct 24, 2019
Version: 3
Version Date: Sep 16, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Settings depending on computer used to run code.
On AMD D drive, downloading all prices: 1 min 35 secs
On AMD C drive, downloading all prices: 0 min 34 secs

Version Notes:
1.1: Changed AMD processor max to usecores - 4.  With Python 3.8.1 update started getting errors when processors was 61 or higher.  So made max 60.
1.2: Simplified code and added Surface Laptop.
2.0: Converted Computer settings scheme to a class object scheme.
2.1: Made computer switching automatically detected.
2.2: Added Amazon Cloud9 configuration.
3.0: Incorporating OOP and overhauling backtesting framework to include win lose profile tester and cloud curve grapher.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS

import psutil
import platform


class Machine():

    __machineprofiles = {
        'DESKTOP-JONUP29': {
            'name': 'surfacepro',
            'dataroot': 'C:/Users/david/David\'s Stuff/CLIMB_DATA',
            'numcore_offset': -1
        },
        'DESKTOP-CATJPV0': {
            'name': 'amdcomp',
            'dataroot': 'D:/CLIMB_DATA',
            'numcore_offset': -4
        },
        'DESKTOP-NPIIPSJ': {
            'name': 'intelcomp',
            'dataroot': 'D:/CLIMB_DATA',
            'numcore_offset': -1
        },
        'DESKTOP-RTO9C0J': {
            'name': 'dadcomp',
            'dataroot': 'C:/Users/david/OneDrive/Documents/CLIMB_DATA',
            'numcore_offset': -1
        },
        'aws-beanstalk': {
            'name': 'awsbeanstalk',
            'dataroot': '~/CLIMB_DATA',  # '/efs/CLIMB_DATA'  '/home/ec2-user/environment/EBS',
            'numcore_offset': 0
        }
    }

    def __init__(self):
        # get current machine info
        try:
            compid = platform.uname().node
        except AttributeError:
            compid = platform.uname()[1]

        # check if machine is on AWS
        if "us-west-1" in compid:
            compid = "aws-beanstalk"
            
        # check if machine has been registered
        if compid not in self.__machineprofiles:
            raise ValueError("This machine has not been configured to be used with this software.")

        # set machine-specific variables
        self.machinename = self.__machineprofiles[compid]['name']
        self.dataroot = self.__machineprofiles[compid]['dataroot']
        # set number of available cpu cores
        num_cores = psutil.cpu_count(logical=True)
        self.use_cores = num_cores - self.__machineprofiles[compid]['numcore_offset']


# instantiate machine
_machine = Machine()
