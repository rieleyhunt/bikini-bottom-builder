#!/bin/bash
t=$1; p=$2
node $(dirname "$0")/gen.js 0 $t 200 200 $p $(dirname "$0")/work/t$t.gba && python3 $(dirname "$0")/place.py $(dirname "$0")/work/t$t.gba 0 $(dirname "$0")/work/t$t.npy 130 228 > /dev/null 2>&1 || echo "FAIL $t"
rm -f $(dirname "$0")/work/t$t.gba
