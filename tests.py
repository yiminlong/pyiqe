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
    
    # def test_QueryMultipleResult(self):
    #     # retrieve a result known to have multiple results
    #     device_id = "pyiqe.test.%s" % time.time()
    #     response, qid = self.api.query('testdata/multipleresult.jpeg', extra={'a':1}, device_id=device_id, multiple_results=True)
    #     print qid
    #     
    #     result = self.api.update(device_id=device_id)
    #     pprint(result)
    #     self.assertTrue(len(result['data']['results'][0]['qid_data']) > 1, "Invalid Multiple Result Return")

class TestTrainingAPI(unittest.TestCase):
    def setUp(self):
        from pyiqe import Api
        self.api = Api(version="1.2")


    def tearDown(self):
        rs_delete = self.api.objects.delete(self.obj_id)
        print rs_delete
        self.assertTrue(rs_delete['error'] == 0)
        
    
    def test_CreateObjectandDelete(self):
        import time
        import os.path as P

        # parameters

        imgpath = P.join(P.dirname(P.abspath(__file__)), "testdata/fox.jpeg")
        name = str(time.time())

        # train the system
        rs_training = self.api.objects.create(
            name = name,
            images = [imgpath], 
            custom_id = "123"
        )
        
        print "Training API response =", rs_training
        self.assertTrue(rs_training['error'] == 0, "Training API request failed")
        
        # try retrieving it
        obj_id = rs_training['obj_id']
        self.obj_id = obj_id
        rs_get = self.api.objects.get(obj_id)
        self.assertTrue(rs_get['object']['obj_id'] == obj_id, "Retrieval Failed")
        
        # wait 10 seconds before querying
        time.sleep(10)

        # query the system for the image
        rs_query, qid = self.api.query(imgpath=imgpath)
        print "Query API response =", rs_query
        print "qid =", qid
        self.assertTrue(rs_query['data']['error'] == 0, "Query API request failed")
        
        # retrieve the results
        for i in range(20):
            rs_result = self.api.result(qid)
            print "Result API response =", rs_result
            assert rs_result['data']['error'] == 0, "Result API request failed"
            if rs_result['data'].has_key('results'):
                break
            time.sleep(1)

        self.assertTrue(rs_result['data'].has_key('results'), "Result API did not return any result after 20 tries")
        self.assertTrue(rs_result['data']['results']['labels'] == name, "Result API does not return correct labels")
        self.assertTrue(rs_result['data']['results']['obj_id'] == rs_training['obj_id'], "Result API does not return correct labels")

class RestfulImagesApi(unittest.TestCase):
    def setUp(self):
        from pyiqe import Api
        self.api = Api(version="1.2")
        
    def testGetImage(self):
        rs_get = self.api.images.get('cc16e9b6f1be4013b53a817a1eea5bdd')
        self.assertTrue(rs_get['error'] == 0, "Unsucessfully retrieve image")
        self.assertTrue(rs_get['image']['img_id'] == 'cc16e9b6f1be4013b53a817a1eea5bdd', "mismatched image id")
    
    def testNonExistentImage(self):
        rs_get = self.api.images.get('cc16e9b6f1be7773b53a817a1eea5bdd')
        self.assertTrue(rs_get['error'] == 1, "No error was thrown for a non-existing image")