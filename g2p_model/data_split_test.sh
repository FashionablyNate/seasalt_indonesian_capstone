#!/usr/bin/env bash

function train_models() {
    
    g2p.py --train train.lex --devel 5% --write-model model-1
    g2p.py --model model-1 --test test.lex > test1.out
}

for ((i = 20; i < 100; i += 10)); do
    cd ${i}_percent_test
    result="$(train_models)"
    cd ../.
done