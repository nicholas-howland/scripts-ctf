#!/bin/bash
## A script to parse ffuf json output files

if [[ $2 == "-s" ]]; then
        STATUS=$3;
else
        STATUS="";
fi

if [[ $1 ]] ; then
        if [[ $STATUS != "" ]]; then
                echo "Results for $1 with status of $STATUS:"
        else
                echo "Results for $1 with any status:"
        fi
        cat $1 | jq -c '.results[] | {url:.url,status: .status}' | grep :$STATUS
else
        echo "Usage: ffuf-parse.sh [ffuf-output-file] -s [status]"
        echo "please supply a ffuf output file"
fi
