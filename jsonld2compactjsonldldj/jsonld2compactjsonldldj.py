#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import json
import sys
import requests
from multiprocessing import Pool,current_process
import ijson.backends.yajl2_cffi as ijson
from pyld import jsonld

def init_mp(c,rf,url,pr,bn):
    global context
    global context_url
    global record_field
    global pathprefix
    global node
    pathprefix=pr
    context=c
    if bn:
        node=True
    else:
        node=False
    if url:
        context_url=url
    else:
        context_url=None
    if rf:
        record_field=rf
    else:
        record_field=None

def compact_object(jsonobject):
    dnb_split=True
    if isinstance(jsonobject,list) and len(jsonobject)==1:
        jsonobject=jsonobject[0]
    if isinstance(jsonobject, dict):
        if (record_field and record_field in jsonobject) or (record_field is None):
            compacted = jsonld.compact(jsonobject, context,  {'skipExpansion': True})
            if context_url:
                compacted['@context'] = context_url#
            if (node and compacted.get("@id") and compacted.get("@id").startswith("_:")) or (node and compacted.get("id") and compacted.get("id").startswith("_:")):
                with open(pathprefix+str(current_process().name)+"-bnodes.ldj","a") as fileout:           ###avoid raceconditions
                    fileout.write(json.dumps(compacted, indent=None) + "\n")
            else:
                with open(pathprefix+str(current_process().name)+".ldj","a") as fileout:
                    fileout.write(json.dumps(compacted, indent=None) + "\n")
            
def yield_obj(path,basepath):
    with open(path,"rb") as fin:
        builder=ijson.common.ObjectBuilder()
        for prefix,event,val in ijson.parse(fin):
            try:
                builder.event(event,val)
            except:
                if hasattr(builder,"value"):
                    sys.stderr.write("error in json: "+str(builder.value)+"\n")
            if prefix==basepath and event=="end_map":
                if hasattr(builder,"value"):
                    yield builder.value
                builder=ijson.common.ObjectBuilder()


def run():
    parser = argparse.ArgumentParser(prog='jsonld2compactjsonldldj',
                                     description='Transforms a given JSON-LD record array to line-delimited, compact JSON-LD records',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    optional_arguments = parser._action_groups.pop()

    required_arguments = parser.add_argument_group('required arguments')
    required_arguments.add_argument('-context-url', type=str, dest='context_url',required=True,
                                    help='A JSON-LD context URL that should be set to reference to the JSON-LD context (instead of inline the JSON-LD context)')

    required_arguments.add_argument('-input', type=str, help='the input JSON-LD record array')
    optional_arguments.add_argument('-record-field', type=str, dest='record_field',
                                    help='A field that should be contained in all records, e.g., a record identifier (this field will be used to identify records)')
    optional_arguments.add_argument('-prefix',type=str,default="chunks/record-",help="a prefix for the multiprocessed outputfiles, could also be a path",dest="prefix")
    
    optional_arguments.add_argument('-split-bnodes',dest="bnode",action="store_true",help="activate this switch to seperate bnodes into extra chunks")

    parser._action_groups.append(optional_arguments)

    args = parser.parse_args()
    process(args.input,args.record_field,args.context_url,args.prefix,args.bnode)


#put this into a function to able to use jsonld2compactjsonldldj as a lib
def process(input,record_field,context_url,pathprefix,bnode):
    r=requests.get(context_url)
    if r.ok:
        jsonldcontext=r.json()
        sys.stderr.write("got context from "+context_url+"\n")
    else:
        sys.stderr.write("unable to get context from {}. aborting\n".format(context_url))
        exit(-1)
    
    pool = Pool(12,initializer=init_mp,initargs=(jsonldcontext,record_field,context_url,pathprefix,bnode,))
    #init_mp(jsonldcontext,record_field,context_url,pathprefix,bnode)
    #item.item = go down 2 (array-)levels as in jsonld-1.1 spec
    for obj in yield_obj(input,"item.item"):
        #compact_object(obj)
        pool.apply_async(compact_object,(obj,))
    pool.close()
    pool.join()

if __name__ == "__main__":
    run()
