"""
nose tests for distance.py 
"""
from distance import calc_duration_close
from distance import calc_duration_open

def test_controls():

    assert calc_duration_close(0,600) == [1, 0]
    assert calc_duration_close(0, 1000) == [1, 0]
    assert calc_duration_open(0, 200) == [0, 0]
    assert calc_duration_open(0, 600) == [0, 0]

def test_ends():

    assert calc_duration_open(400,600) ==  [12, 8]
    
def test_endOfRide():

    assert calc_duration_close(600,600) == calc_duration_close(603,600)
    assert calc_duration_open(200, 200) == calc_duration_open(210,200)
