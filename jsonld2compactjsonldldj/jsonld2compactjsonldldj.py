#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import json
import sys

from pyld import jsonld


def run():
    parser = argparse.ArgumentParser(prog='jsonld2compactjsonldldj',
                                     description='Transforms a given JSON-LD record array to line-delimited, compact JSON-LD records',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    optional_arguments = parser._action_groups.pop()

    required_arguments = parser.add_argument_group('required arguments')
    required_arguments.add_argument('-context', type=str, help='The JSON-LD context file', required=True)

    optional_arguments.add_argument('-input', type=str, help='the input JSON-LD record array')
    optional_arguments.add_argument('-record-field', type=str, dest='record_field',
                                    help='A field that should be contained in all records, e.g., a record identifier (this field will be used to identify records)')
    optional_arguments.add_argument('-context-url', type=str, dest='context_url',
                                    help='A JSON-LD context URL that should be set to reference to the JSON-LD context (instead of inline the JSON-LD context)')

    parser._action_groups.append(optional_arguments)

    args = parser.parse_args()

    context = args.context

    with open(context, newline='') as contextfile:
        jsonldcontext = json.load(contextfile)

    record_field = None

    if args.record_field is not None:
        record_field = args.record_field

    context_url = None

    if args.context_url is not None:
        context_url = args.context_url

    if args.input is not None:
        with open(args.input, newline='') as inputfile:
            jsonldarray = json.load(inputfile)
    else:
        jsonldarray = json.load(sys.stdin)

    options = {'skipExpansion': True}

    if isinstance(jsonldarray, list):
        for innerjsonarray in jsonldarray:
            if isinstance(innerjsonarray, list):
                for jsonobject in innerjsonarray:
                    if isinstance(jsonobject, dict):
                        if (record_field is not None and record_field in jsonobject) or (record_field is None):
                            compacted = jsonld.compact(jsonobject, jsonldcontext, options)
                            if context_url is not None:
                                compacted['@context'] = context_url
                            sys.stdout.write(json.dumps(compacted, indent=None) + "\n")


if __name__ == "__main__":
    run()
