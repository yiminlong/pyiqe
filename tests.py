import time
import unittest    
from pprint import pprint 

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
        import json
        device_id = "pyiqe.test.%s" % time.time()
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
        
    
    def test_QueryMultipleResult(self):
        # retrieve a result known to have multiple results
        device_id = "pyiqe.test.%s" % time.time()
        response, qid = self.api.query('testdata/multipleresult.jpeg', extra={'a':1}, device_id=device_id, multiple_results=True)
        print qid
        
        result = self.api.update(device_id=device_id)
        pprint(result)
        assert len(result['data']['results'][0]['qid_data']) > 1, "Invalid Multiple Result Return"

