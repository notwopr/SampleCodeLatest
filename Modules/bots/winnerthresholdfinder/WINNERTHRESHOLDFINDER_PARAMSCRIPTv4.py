"""
Title: WINNERTHRESHOLD FINDER PARAMSCRIPT
Date Started: Feb 7, 2021
Version: 4.00
Version Start Date: Feb 7, 2021
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Description:
v1 and v2 combined, no dupes, no weight changes
"""
from genericfunctionbot import scriptjoiner_removedupes

scriptlist = [
    {
        'scriptnickname': 'winnerthresholdfinderv1',
        'scriptfilename': 'WINNERTHRESHOLDFINDER_PARAMSCRIPTv1',
        'scriptweight': 1
    },
    {
        'scriptnickname': 'winnerthresholdfinderv2',
        'scriptfilename': 'WINNERTHRESHOLDFINDER_PARAMSCRIPTv2',
        'scriptweight': 1
    }
]
stage3_params = scriptjoiner_removedupes(scriptlist, 'winnerthresholdfinderv4')
