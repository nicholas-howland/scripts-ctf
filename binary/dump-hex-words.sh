#!/bin/bash
cat /usr/share/dict/american-english | grep --ignore-case "^[ABCDEFGILOSZ]*$" | sed 's/[gG]/6/g;s/[iI]/1/g;s/[lL]/1/g;s/[oO]/0/g;s/[sS]/5/g;s/[zZ]/2/g' | tr [:lower:] [:upper:]
