#!/usr/bin/env bash

function train_models() {
    
    g2p.py --train train.lex --devel 5% --write-model model-1
    g2p.py --model model-1 --test test.lex > test1.out

    g2p.py --model model-1 --ramp-up --train train.lex --devel 5% --write-model model-2
    g2p.py --model model-2 --test test.lex > test2.out

    g2p.py --model model-2 --ramp-up --train train.lex --devel 5% --write-model model-3
    g2p.py --model model-3 --test test.lex > test3.out

    g2p.py --model model-3 --ramp-up --train train.lex --devel 5% --write-model model-4
    g2p.py --model model-4 --test test.lex > test4.out

    g2p.py --model model-4 --ramp-up --train train.lex --devel 5% --write-model model-5
    g2p.py --model model-5 --test test.lex > test5.out

    g2p.py --model model-5 --ramp-up --train train.lex --devel 5% --write-model model-6
    g2p.py --model model-6 --test test.lex > test6.out

    g2p.py --model model-6 --ramp-up --train train.lex --devel 5% --write-model model-7
    g2p.py --model model-7 --test test.lex > test7.out

    g2p.py --model model-7 --ramp-up --train train.lex --devel 5% --write-model model-8
    g2p.py --model model-8 --test test.lex > test8.out

    g2p.py --model model-8 --ramp-up --train train.lex --devel 5% --write-model model-9
    g2p.py --model model-9 --test test.lex > test9.out

    g2p.py --model model-9 --ramp-up --train train.lex --devel 5% --write-model model-10
    g2p.py --model model-10 --test test.lex > test10.out
}

for ((i = 10; i < 100; i += 10)); do
    cd ${i}_percent_test
    result="$(train_models)"
    cd ../.
done