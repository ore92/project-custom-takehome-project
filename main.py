import random, requests, json, unittest, numpy as np

from enum import Enum,auto
from statistics import mean, mode, harmonic_mean
from requests.exceptions import HTTPError
from unittest.mock import patch
    
class MoctType(Enum):
    """
    Enum to represent the various Moct: measure of central tendencies allowed.
    """ 
    ArithmeticMean = auto()
    GeometricMean = auto()
    Mode = auto()
    HarmonicMean = auto()
    Random = auto()
    
def coalesce(apis, member_id, moct):
    """
    coalesce takes 3 apis and passes the member_id param and coalesces the response

    :param apis: the list of apis being called,must be at least length 3
    :param member_id: the member_id
    :param moct: the measure of central tendency
    :returns: a json object of the coalesced values (deductibe, stop_loss, oop_max) 
    """ 
    (deductible1, stop_loss1, oop_max1) = call_api(api[0],member_id)
    (deductible2, stop_loss2, oop_max2) = call_api(api[1],member_id)
    (deductible3, stop_loss3, oop_max3) = call_api(api[2],member_id)
    
    deductibles = [deductible1, deductible2, deductible3]
    stop_losses = [stop_loss1, stop_loss2, stop_loss3]
    oop_maxes = [oop_max1, oop_max2, oop_max3]
    
    deductible = find_mean(deductibles, moct)
    stop_loss = find_mean(stop_losses, moct)
    oop_max = find_mean(oop_maxes, moct)
    
    json_return = {
        "deductible": deductible,
        "stop_loss": stop_loss,
        "oop_max": oop_max
    }
    
    return json.dumps(json_return)
    

def find_mean(datapoints, moct):
    """
    find_mean returns a mean for datapoints; defaults to arithmetic mean

    :param datapoints: a list of numerical values/datapoints
    :param moct: the measure of central tendency e.g mode etc
    :returns: a  mean, a single value representing the datapoints
    """ 
    if moct == MoctType.Mode:
        return mode(datapoints)
    elif moct == MoctType.HarmonicMean:
        return harmonic_mean(datapoints)
    elif moct == MoctType.Random:
        return random.choice(datapoints)
    elif moct == MoctType.ArithmeticMean: #colloquial average
        return mean(datapoints)
    elif moct == MoctType.GeometricMean:
        x = np.array(datapoints)
        return x.prod()**(1.0/len(x))
    else:
        raise ValueError("Invalid mean type "+ str(moct))

def call_api(url,member_id):
    """
    call_api makes a call to url with memeber_id as param

    :param url: the api being called
    :param member_id: the member_id
    :returns: a tuple with (deductibe, stop_loss, oop_max) for member_id
    """ 
    try:
        payload = {'id': id}
        response = requests.get(url, payload)
        response.raise_for_status()
        jsonResponse = response.json()
        deductible = jsonResponse["deductible"]
        stop_loss = jsonResponse["stop_loss"]
        oop_max = jsonResponse["oop_max"]
        return (deductible, stop_loss, oop_max)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def choice0(data):
    """
    chhoice0 returns the first value in date as the moct

    :param data: a list of numerical values/datapoints
    """ 
    return data[0]
        
class TestMethods(unittest.TestCase):   
    
    def test_find_mean_mode(self):
        self.assertEqual(find_mean([1,2,3,1],MoctType.Mode),1)
    
    def test_find_mean_geometric_mean(self):
        self.assertEqual(find_mean([1,2,3,1],MoctType.ArithmeticMean),1.75)
        
    def test_find_mean_geometric_mean(self):
        self.assertEqual(find_mean([1,2,2,4],MoctType.GeometricMean),2.0)
    
    def test_find_mean_harmoic_mean(self):
        self.assertEqual(find_mean([1,2,3,4],MoctType.HarmonicMean),1.92)
        
    @patch('random.choice', choice0)  
    def test_find_mean_random(self):
        self.assertEqual(find_mean([1,2,3,4],MoctType.Random),1)
        
if __name__ == '__main__':
    unittest.main(exit=False)
