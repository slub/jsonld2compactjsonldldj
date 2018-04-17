#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import json
import sys
import requests
from multiprocessing import Pool,current_process
from pyld import jsonld

def init_mp(m,c,rf,url):
    global mp
    global context
    global context_url
    global record_field
    mp=m
    context=c
    if url:
        context_url=url
    else:
        context_url=None
    if rf:
        record_field=rf
    else:
        record_field=None

def compact_object(jsonobject):
    if isinstance(jsonobject, dict):
        if (record_field and record_field in jsonobject) or (record_field is None):
            compacted = jsonld.compact(jsonobject, context,  {'skipExpansion': True})
            if context_url:
                compacted['@context'] = context_url
            if mp:
                with open(str(current_process().name)+"-records.ldj","a") as fileout:           ###avoid raceconditions
                    fileout.write(json.dumps(compacted, indent=None) + "\n")
            else:
                sys.stdout.write(json.dumps(compacted, indent=None) + "\n")
            
def run():
    parser = argparse.ArgumentParser(prog='jsonld2compactjsonldldj',
                                     description='Transforms a given JSON-LD record array to line-delimited, compact JSON-LD records',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    optional_arguments = parser._action_groups.pop()

    required_arguments = parser.add_argument_group('required arguments')
    required_arguments.add_argument('-context', type=str, help='The JSON-LD context file')

    optional_arguments.add_argument('-input', type=str, help='the input JSON-LD record array')
    optional_arguments.add_argument('-record-field', type=str, dest='record_field',
                                    help='A field that should be contained in all records, e.g., a record identifier (this field will be used to identify records)')
    optional_arguments.add_argument('-context-url', type=str, dest='context_url',
                                    help='A JSON-LD context URL that should be set to reference to the JSON-LD context (instead of inline the JSON-LD context)')
    optional_arguments.add_argument('-mp', action="store_true",
                                    help='Switch on to use Multiprocessing')


    parser._action_groups.append(optional_arguments)

    args = parser.parse_args()

    if args.context_url:
        r=requests.get(args.context_url)
        if r.ok:
            jsonldcontext=r.json()
            sys.stderr.write("got context from "+args.context_url+"\n")
    elif args.context:
        with open(args.context, newline='') as contextfile:
            jsonldcontext = json.load(contextfile)
    else:
        sys.stderr.write("got no context-file or url. aborting\n")
        exit(-1)
        
    if args.input is not None:
        with open(args.input, newline='') as inputfile:
            jsonldarray = json.load(inputfile)
    else:
        jsonldarray = json.load(sys.stdin)

    #options = {'skipExpansion': True}
    if args.mp:
        pool = Pool(initializer=init_mp,initargs=(args.mp,jsonldcontext,args.record_field,args.context_url,))
    else:
        init_mp(args.mp,jsonldcontext,args.record_field,args.context_url)
    if isinstance(jsonldarray, list):
        for innerjsonarray in jsonldarray:
            if isinstance(innerjsonarray, list):
                if args.mp:
                    pool.map(compact_object,innerjsonarray)
                else:
                    for jsonobject in innerjsonarray:
                        compact_object(jsonobject)
                    
if __name__ == "__main__":
    run()
