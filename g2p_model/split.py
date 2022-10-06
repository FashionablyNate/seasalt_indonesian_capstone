import random
import sys

def main():

    if ( len( sys.argv ) != 3 ):
        print( "Useage: " + sys.argv[0] + " <lexicon> <percentage of lexicon in test.lex>" )
        return -1

    input_file = sys.argv[1]
    test_percent = sys.argv[2]

    test = []
    train = []

    lexicon_txt = open( input_file, 'r' );

    for line in lexicon_txt.readlines():
        if random.randint( 0, 100 ) < int( test_percent ):
            test.append( line )
        else:
            train.append( line )

    lexicon_txt.close()

    test_lex = open( 'test.lex', 'w' )
    test_lex.writelines( test )
    test_lex.close()

    train_lex = open( 'train.lex', 'w' )
    train_lex.writelines( train )
    train_lex.close()

    return 0

main()