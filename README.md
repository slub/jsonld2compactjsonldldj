# jsonld2compactjsonldldj - JSON-LD to compact JSON-LD line-delimited JSON records transformator

jsonld2compactjsonldldj is a commandline command (Python3 program) that transforms a given JSON-LD record array to line-delimited, compact JSON-LD records

It (usually) reads from stdin and prints to stdout.

## Usage

```
jsonld2compactjsonldldj

required arguments:
  -context CONTEXT              The JSON-LD context file (default: None)

optional arguments:
  -h, --help                    show this help message and exit
  -input INPUT                  the input JSON-LD record array (default: None)
  -record-field RECORD_FIELD    A field that should be contained in all records, e.g., a record identifier (this field will be used to identify records) (default: None)
  -context-url CONTEXT_URL      A JSON-LD context URL that should be set to reference to the JSON-LD context (instead of inline the JSON-LD context) (default: None)
```

* example:
    ```
    jsonld2compactjsonldldj -context [PATH TO THE JSON-LD CONTEXT FILE] < [PATH TO THE INPUT JSON-LD FILE] > [PATH TO THE OUPUT JSON-LD LINE-DELIMITED JSON RECORDS FILE]
    ```

### Note

This program is not optimized for processing of large input files at the moment, i.e., there is no parallelization involved nor stream processing. So processing larger input files requires much (free) RAM and a bit of time ;)

## Requirements

[PyLD](https://github.com/digitalbazaar/pyld)

e.g.
```
sudo -H pip3 install PyLD
```

## Run

* install PyLD
* clone this git repo or just download the [jsonld2compactjsonldldj.py](jsonld2compactjsonldldj/jsonld2compactjsonldldj.py) file
* run ./jsonld2compactjsonldldj.py
* for a hackish way to use jsonld2compactjsonldldj system-wide, copy to /usr/local/bin

### Install system-wide via pip

```
sudo -H pip3 install --upgrade [ABSOLUTE PATH TO YOUR LOCAL GIT REPOSITORY OF JSONLD2COMPACTJSONLDLDJ]
```
(which provides you ```jsonld2compactjsonldldj``` as a system-wide commandline command)