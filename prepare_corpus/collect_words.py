
import os
import re
import string
from prepare_commonvoice import text_proc

rootDir = './commonvoice-root'
file_list = []
word_list = set()
new_word_list = set()

for (root, dirs, files) in os.walk(rootDir):
    file_list = filter( lambda n: re.search( ".tsv", str(n) ), files )
    for tsv_file in file_list:
        f = open( root + "/" + tsv_file )
        count = 0
        for line in f:
            if count == 0:
                count += 1
                continue
            for x in line.split():
                if not any(chr.isdigit() for chr in x):
                    word_list.add( x )
        f.close()

word_list = filter( lambda n: not re.search( "grammar-or-spelling", str(n) ), word_list )
word_list = filter( lambda n: not re.search( "id", str(n) ), word_list )
word_list = filter( lambda n: not re.search( "difficult-pronounce", str(n) ), word_list )
word_list = filter( lambda n: not re.search( "different-language", str(n) ), word_list )
word_list = filter( lambda n: not re.search( "offensive-language", str(n) ), word_list )
word_list = filter( lambda n: not re.search( "difficult-pronunciation", str(n) ), word_list )

new_lexicon = open("commonvoice_lexicon.txt", "w")
word_list = list(word_list)
word_list.sort()
for word in word_list:
    new_word_list.add(text_proc(word.translate(str.maketrans('', '', string.punctuation))).lower() + "\n")

new_word_list = list(new_word_list)
new_word_list.sort()

for word in new_word_list:
    new_lexicon.write( word )

new_lexicon.close()