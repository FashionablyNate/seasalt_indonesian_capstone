#!/usr/bin/env bash

function train_models() {
    
    echo "Training model-1"
    last=1
    g2p.py --train train.lex --devel 5% --write-model model-1
    for ((i = 2; i < 9; i++)); do
        echo "Training model ${i} from model ${last}"
        g2p.py --model model-${last} --ramp-up --train train.lex --devel 5% --write-model model-${i}
        last=${i}
    done
    echo "Testing model-${last}"
    g2p.py --model model-${last} --test test.lex > test.out
}

result="$(train_models)"