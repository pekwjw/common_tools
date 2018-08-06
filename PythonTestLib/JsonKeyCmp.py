# -*- coding:utf-8 -*-

import json
import types
from LoggerInit import *
from HttpRelate import * 

a_whitelist = []
b_whitelist = []
type_whitelist = []

_TYPE_DICT = type(dict())
_TYPE_LIST = type(list())
_TYPE_TUPLE = type(tuple())
_TYPE_INT = type(int())
_TYPE_STR = type(str())

info_log = setup_common_logger('infolog')
err_log = setup_common_logger('errlog') 

def field_value_type_cmp(a_body,b_body,prefix = '',infolog = info_log,errlog = err_log):   
    if type(a_body) == type(b_body):
        infolog.info("TYPE EQUAL: " + prefix + ' ' + str(type(a_body)))
        if type(a_body) == type(dict()):
            dict_key_cmp(a_body,b_body,prefix)
        elif type(a_body) == type(list()):
            list_key_cmp(a_body[0],b_body[0],prefix)
        elif type(a_body) == type(tuple()):
            list_key_cmp(a_body[0],b_body[0],prefix)
        else:
            pass
    else:
        errlog.error("TYPE NOT EQUAL: " + prefix + ":" + ' a_body is: ' + str(type(a_body)) + ' b_body is: ' + str(type(b_body)))

def list_key_cmp(a_list,b_list,prefix = '',infolog = info_log,errlog = err_log):
    if type(a_list) == type(b_list):
        infolog.info("TYPE EQUAL: " + prefix + " " + str(type(a_list)))
        if type(a_list) == type(dict()):
            dict_key_cmp(a_list,b_list,prefix+' 0/')
        elif type(a_list) == type(list()):
            list_key_cmp(a_list[0],b_list[0],prefix+' 0/')
        elif type(a_list) == type(tuple()):
            list_key_cmp(a_list[0],b_list[0],prefix+' 0/')
        else:
            pass
    else:
        errlog.error("TYPE NOT EQUAL: " + prefix + ' a_body is: ' + str(type(a_list[0])) + ' b_body is: ' + str(type(b_list[0])))

def dict_key_cmp(dicta,dictb,prefix = '',flag = 1,infolog = info_log,errlog = err_log):
    """Compare two dicts' key, and print ERROR to Screen or record the difference to errlog.
    Args:
        dicta: dict
            the input dict A.
        dictb: dict
            the input dict B.
        prefix: str
            describe the node of dict's location.
        flag: int
            if flag == 1: call the field_value_type_cmp to compare the dicta and dictb's commom keys' value's type; 
            if flag != 1: only compare the dicta and dictb keys' difference.
    Returns: nothing
    Result: the difference of dicta and dictb will print to Screen or record into errlog. 
    """
    prefix = prefix + '/'
    a_keys = set(dicta.keys())
    b_keys = set(dictb.keys())
    ab_common = a_keys & b_keys
    a_sub = (a_keys - ab_common) - set(a_whitelist)
    b_sub = (b_keys - ab_common) - set(b_whitelist)
    if a_sub:
        fields = ','.join(a_sub) 
        errlog.error("KEY_A_ONLY: " + prefix + ":" + fields)
    if b_sub:
        fields = ','.join(b_sub)
        errlog.error("KEY_B_ONLY: " + prefix + ":" + fields)
    if ab_common and flag:
        for _,field in enumerate(ab_common):
            field = field.encode('utf-8')
            field_value_type_cmp(dicta[field],dictb[field],prefix+field+'/')

def json_key_cmp(jsona,jsonb,prefix = '',infolog = info_log,errlog = err_log):
    """Compare two jsons' key, and print ERROR to Screen or record the difference to errlog.
    Args:
        jsona: dict or list
            the input json body A.
        jsonb: dict or list
            the input json body B.
        prefix: str
            describe the node of json body's location.
    Returns: nothing
    Result: the difference of jsona and jsonb will print to Screen or record into errlog.
    """
    if type(jsona) == type(jsonb):
        if type(jsona) == _TYPE_DICT:
            dict_key_cmp(jsona,jsonb,prefix = '')
        elif type(jsona) == _TYPE_LIST:
            list_key_cmp(jsona,jsonb,prefix = '')
        elif type(jsona) == _TYPE_TUPLE:
            list_key_cmp(jsona,jsonb,prefix = '')
        else:
            errlog.warning("jsona and jsonb types is equal,but not in [dict,list,tupe],cannot deal!")
            pass
    else:
        errlog.critical("jsona and jsonb type is not equal,cannot compare!")
   
def main():
    pass

if __name__ == "__main__":
    main()
