# -*- coding: UTF-8 -*-

STABLE_API_VERSION = "1.2"

def Api(version=STABLE_API_VERSION, *args, **kwargs):
    """
    A shortcut method for generating api instances given the version number,
    if no version number is given, it defaults to the most current stable
    IQEngines Api Version.
    
    For further information see the docstrings for the following classes:
    
    pyiqe.apis.api1_2.Api
    pyiqe.apis.api1_3.Api
    
    
    """
    import apis.api1_2
    import apis.api1_3
    api_map  = {
        "1.2" : apis.api1_2.Api,
        "1.3" : apis.api1_3.Api,
    }
    if not version in api_map:
        raise Exception("Invalid Api Version")
    ApiClass = api_map[version]
    return ApiClass(*args, **kwargs)
