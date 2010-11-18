# -*- coding: UTF-8 -*-
__all__ = ['Api']

import apis.api1_2
STABLE_API_VERSION = "1.2"

def Api(*args, **kwargs):
    """
    This is a thin wrapper around the Actual API Instances.
    
    Usage
    -----
    
    iqe = Api(KEY,SECRET, version="1.2")
    
    For further information see the docstrings for the following classes:
    
    pyiqe.apis.api1_2.Api
    """
    
    version = kwargs.pop('version', STABLE_API_VERSION)

    api_map  = {
        "1.2" : apis.api1_2.Api,
    }
    if not version in api_map:
        raise Exception("Invalid Api Version")
    ApiClass = api_map[version]
    return ApiClass(*args, **kwargs)
