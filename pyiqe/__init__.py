import os
import simplejson
import hmac
from hashlib import sha1

class Api(object):
    """
    Handles requests to the IQ Engines API. An API object is initialized using the API key and secret::
    
        >>> from pyiqe import Api
        >>> api = Api(API_KEY, SECRET)
    
    You can quickly query an image and retrieve results by doing::
    
        >>> data, qid = api.query("/path/to/img.jpg")
        >>> data
        {u'data': {u'error': 0}}
        >>> qid
        '74235664e1f1fc643a15e44517a4cf3d3cbd6874'
        >>> results = api.update()
        >>> results
        {u'data': {u'error': 0,
                   u'results': [{u'qid': u'74235664e1f1fc643a15e44517a4cf3d3cbd6874',
                                 u'qid_data': {u'color': u'Mostly brown orange, with some yellow blue black.',
                                               u'labels': u'Duracell Batteries'}}]}}
    
    Update API is a long-polling request. As soon as IQ Engines has tagged your image, it'll output your results!
    """
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
    
    def _now(self):
        from datetime import datetime
        t = datetime.utcnow()
        return t.strftime("%Y%m%d%H%M%S")
    
    def _build_signature(self, fields, files=None):
        # put the parameters in a dictionary
        params = dict((key, value) for key, value in fields)
        if files:
            if files[0][0] == "img":
                img = os.path.split(files[0][1])[1]
                params.update(dict(img=img))
        # reorder the parameters and join key value pairs together
        sorted_params = sorted( ( key,value ) for key,value in params.iteritems() )
        raw_string = "".join(["".join(x) for x in sorted_params])
        # compute secret
        digest_maker = hmac.new(self.secret, raw_string, sha1)
        return digest_maker.hexdigest()
    
    def _post(self, selector, fields=None, files=None, json=False):
        fields = fields if fields else []
        files = files if files else []
        fields.append(("time_stamp", self._now()))
        fields.append(("api_key", self.key))
        if json:
            fields.append(("json", "1"))
        # build signature
        sig = self._build_signature(fields, files)
        fields.append(("api_sig", sig))
        # POST the form
        from utils import post_multipart
        res = post_multipart("api.iqengines.com", "http", "/v1.2/%s/"%selector, fields, files).read()
        if json:
            res = simplejson.loads(res)
        return res, sig
    
    def query(self, imgpath=None, imgdata=None, webhook=None, json=True):
        """
        :type imgpath: string
        :param imgpath: Path to the image you want to have tagged
        
        :type imgdata: string
        :param imgpath: binary image data

        :type webhook: string
        :param webhook: url to post the labels
        
        :type json: boolean
        :param json: If True the output is a Python dictionary, otherwise XML
        
        Submit an image to the IQ Engines image labeling engine using the Query API::
        
            >>> data, qid = api.query('/path/to/img.jpg')
            >>> data
            {u'data': {u'error': 0}}
            >>> qid
            '74235664e1f1fc643a15e44517a4cf3d3cbd6874'
        
        """
        assert imgpath is not None or imgdata is not None, "either imgpath or imgdata required!"
        if imgdata is None: imgdata = open(imgpath).read()
        files  = [ ("img", imgpath or sha1(imgdata).hexdigest(), imgdata) ]
        fields = [("webhook", webhook)] if webhook else None
        data, sig = self._post(selector="query", fields=fields, files=files, json=json)
        return data, sig
    
    def update(self, json=True):
        """
        
        :type json: boolean
        :param json: If True the output is a Python dictionary, otherwise XML
        
        Start a long-polling request to wait for resutls using the Update API::
        
            >>> results = api.update()
            >>> results
            {u'data': {u'error': 0,
                       u'results': [{u'qid': u'74235664e1f1fc643a15e44517a4cf3d3cbd6874',
                                     u'qid_data': {u'color': u'Mostly brown orange, with some yellow blue black.',
                                                   u'labels': u'Duracell Batteries'}}]}}
        
        """
        data, _ = self._post(selector="update", json=json)
        return data
    
    def result(self, qid, json=True):
        """
        :type qid: string
        :param qid: The QID corresponding to the image for which you want to retrieve the labels
        
        :type json: boolean
        :param json: If True the output is a Python dictionary, otherwise XML
        
        Retrieve the results for a specific QID using the Result API::
        
            >>> result = api.result(qid="74235664e1f1fc643a15e44517a4cf3d3cbd6874")
            >>> result
            {u'data': {u'error': 0,
                       u'results': {u'color': u'Mostly brown orange, with some yellow blue black.',
                                    u'labels': u'Duracell Batteries'}}}
        
        """
        data, _ = self._post(selector="result", fields=[("qid", qid)], json=json)
        return data
    



