import re

lexicon_in_A = "lexicon.txt"
lexicon_in_B = "transcribed-commonvoice-lexicon.txt"
lexicon_result = "new_lexicon.txt"

line_list = set()

lexicon_a = open( lexicon_in_A )
for line in lexicon_a:
    line_list.add( line )
lexicon_a.close()

lexicon_b = open( lexicon_in_B )
for line in lexicon_b:
    line_list.add( line.replace(" ", "\t") )
lexicon_b.close()

line_list = list( line_list )
line_list.sort()
lexicon_out = open( lexicon_result, "w" )
for line in line_list:
    lexicon_out.write( line )
lexicon_out.close()