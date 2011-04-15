import unittest    
import time
def test_basic_imports():
    """ Make sure we can atleast import everything """
    from pyiqe import Api
    api = Api()



class TestApi(unittest.TestCase):
    
    def setUp(self):
        from pyiqe import Api
        self.api = Api(version="1.2")
        
    def test_QueryExtra(self):
        """ Make sure we pass back extra argument is returned"""
        import random
        import json
        from pprint import pprint 
        device_id = "pyiqe.test.%s" % random.random()
        response, qid = self.api.query('testdata/dole1.jpeg', extra={'a':1}, device_id=device_id)
        
        # update method
        result = self.api.update(device_id=device_id)
        pprint(result)
        result = result['data']['results']
        pprint(result)
        assert "extra" in result[0] and result[0]['extra'] == json.dumps({'a':1}), "Extra Argument mismatch %s" % result
        
        # result method
        response = self.api.result(qid)
        result = response['data']
        pprint(result)
        assert "extra" in result and result['extra'] == json.dumps({'a':1}), "Extra Argument mismatch %s" % result
        
        
