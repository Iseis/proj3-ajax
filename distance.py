"""Finds the duration from the given control distance and the 
   brevet distance.
   Author: Andrew Owens
"""

import math

### Max time limits for different brevets [hr, min] format
acpMaxLimits = { 200: [13, 30], 300: [20, 00], 400: [27, 00], 600: [40, 00],
                1000: [75, 00]}
                
acp_speed_fast = { 200: 34, 400: 32, 600: 30, 1000: 28 }
acp_speed_slow = { 600: 15, 1000: 11.428 }


"""
calculates the open time for the current control
takes a control and a brevet_length which is the
total
"""
def calc_duration_open(control, brevet_length):
    #if the the contol dist is 0 then we return 0
    if control == 0:
       return [0, 0]
       
    time = 0
    
    # if we are bigger than the brevet_length then our control
    # is the brevet length
    if control > brevet_length:
         control = brevet_length
    
    #needed for final calc
    old_key = 201
    for key in sorted(acp_speed_fast.keys()):
        if control <= 0:
            break
            
        if control < old_key: #calc remainder
           time += control/acp_speed_fast[key]
           control -= control
        else:
           time += 200/acp_speed_fast[key]
           control -= 200
           old_key = key
           
    hour = math.floor(time)
    minutes = time - hour
    minutes = int(round(minutes * 60))
    return [hour, minutes]
 
""" 
Calculates the closing time for the given distance
takes a control arg and a length_arg
"""
def calc_duration_close(control, brevet_length):
    #if the the contol dist is 0 then we return 0
    if control == 0:
       return [1, 0]
       
    time = 0
    
    # if we are >= the brevet_length then return
    # is the brevet length
    if control >= brevet_length:
         return acpMaxLimits[brevet_length]
    
    #add um together
    for key in sorted(acp_speed_slow.keys()):
        if control <= 0:
            break
            
        if control < key: 
           time += control/acp_speed_slow[key]
           control -= control
        else:
           time += 600/acp_speed_slow[key]
           control -= 600
           old_key = key
           
    hour = math.floor(time)
    minutes = time - hour
    minutes = int(round(minutes * 60))
    return [hour, minutes]


