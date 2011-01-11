    
def test_basic_imports():
    """ Make sure we can atleast import everything """
    from pyiqe import Api


def _test_query_flow():
    """ 
    Tests whether querying works with the same interface. Warning, this will deplete your
    purchased query count. Also it requires that you set IQE_KEY and IQE_SECRET in your
    environment
    """
    import time
    from pyiqe import Api
    
    iqe = Api(version="1.2")
    response, qid = iqe.query('testdata/dole1.jpeg')
    print("sending in query with qid %s" % qid)
    assert response == {'data': {'error': 0}}, "Invalid Response while querying: \n%s " % response
    
    print("\nwaiting for results ...")
    response = iqe.update()
    print(response)
    
    print("\nretrieving results manually")
    time.sleep(2)
    response = iqe.result(qid)
    print(response)
    
def _test_query_flow_with_device_id():
    """ 
    Tests whether querying works with the same interface. Warning, this will deplete your
    purchased query count. Also it requires that you set IQE_KEY and IQE_SECRET in your
    environment
    """
    import time
    from pyiqe import Api
    
    iqe = Api(version="1.2")
    response, qid = iqe.query('testdata/dole1.jpeg', device_id="testing.1234")
    print("sending in query with qid %s" % qid)
    assert response == {'data': {'error': 0}}, "Invalid Response while querying: \n%s " % response
    
    print("\nwaiting for results ...")
    response = iqe.update(device_id="testing.1234")
    print(response)
    
    print("\nretrieving results manually")
    time.sleep(2)
    response = iqe.result(qid)
    print(response)

    
