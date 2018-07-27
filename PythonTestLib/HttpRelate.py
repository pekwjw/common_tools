# -*- coding:utf-8 -*-

import urllib2
import json 
import types
import os
from copy import deepcopy

_TYPE_DICT = type(dict())
_TYPE_LIST = type(list())
_TYPE_TUPLE = type(tuple())
_TYPE_INT = type(int())
_TYPE_STR = type(str())

def get_response(url,maxretry=10):
    '''Get json body from the specified url.
    Args:
        url: str
            the specified url.
        maxretry: int
            max retry times,default value is 10. 
    Returns:
        a json body from the url.
    '''
    for tries in range(maxretry):
        try :
            connector = urllib2.urlopen(urllib2.Request(url))
            break
        except :
            if tries <=(maxretry - 1):
                continue
            else :
                print "retry " + str(tries) + " times"
                return False
    return json.loads(connector.read())

def get_value_from_json(json_body,key_path=''):
    '''Analyze the json body to find the specified keys' value.
    Args:
        json_body: dict
            the input json body.
        key_path: str
            the string describe the specified keys' position
    Returns:
        value of the specified keys
    E.G. : body is : {"r":{"data":{"commlist":[{"first":1,"second":2},{"first":3,"second":4}]},"tmpdata":"tmp data"},"tmpfield":"a string"}
           key_path is : r/data/commlist 0 
           return : {"first":1,"second":2}
    '''
    if json_body ==  "": 
        return ""
    if type(json_body) != _TYPE_DICT and type(json_body) != _TYPE_LIST :
        print "ERROR:json_body's type is wrong!"
        return json_body
    if key_path : 
        pathl = key_path.split("/")
        tmpbody = deepcopy(json_body)
        for i,tmp_path in enumerate(pathl): 
            try:
                if " " in tmp_path:
                    tmp_pathl = tmp_path.split(" ")
                    tmpbody = tmpbody[tmp_pathl[0]][int(tmp_pathl[1])]
                else:
                    tmpbody = tmpbody[tmp_path]
            except Exception,err:
                print "ERROR:get " + key_path + " from the given body FAILED!" 
                return 
        return tmpbody
    else :
        return json_body

def get_value_from_url(url,key_path="",maxrety=10):  
    '''Get json body from the specified url,and analyze the response to find the specified keys' value.
    Args:
        url: str
            the specified url.
        key_path: str
            the string describe the specified keys' position
        maxretry: int
            max retry times,default value is 10. 
    Returns:
        value of the specified keys
    E.G. : url response is : {"r":{"data":{"commlist":[{"first":1,"second":2},{"first":3,"second":4}]},"tmpdata":"tmp data"},"tmpfield":"a string"}
           key_path is : r/data/commlist 0 
           return : {"first":1,"second":2}
    '''
    json_body = get_response(url)
    return get_value_from_json(json_body,key_path)

def main():
    pass

if __name__ == "__main__":
    main()
