#!/usr/bin/env bash

mkdir multi_gen_test
cd multi_gen_test

for ((i = 0; i < 10; i++)); do
    python ../split.py ../lexicon.txt 20
    mv test.lex test${i}.lex
    mv train.lex train${i}.lex
    
    g2p.py --train train${i}.lex --devel 5% --write-model model-${i}
    g2p.py --model model-${i} --test test${i}.lex > test${i}.out
done

cd ..