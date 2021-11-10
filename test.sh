#!/bin/sh

echo "Testing the parchmint Files"

for f in ./chthesis/*.json;

do
    echo "Running File $f";
    # fluigi --c $f --out ~/Desktop/MINT/chthesis
    python test.py $f
done