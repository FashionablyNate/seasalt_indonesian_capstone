#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import codecs
import chardet
import os
import re
import sys
from num2words import num2words


decode_hex = codecs.getdecoder("hex_codec")

def get_args():
    parser = argparse.ArgumentParser(description="""
        This script prepares the data folders for the CommonVoice.
        """)
    parser.add_argument('--prefix', type=str, default='commonvoice',
                        help="""Prefix of CommonVoice""")
    parser.add_argument('--input_dir', type=str, required=True,
                        help="""Input dir of CommonVoice""")
    parser.add_argument('--train_dir', type=str, required=True,
                        help="""Output train dir for prepared data""")
    parser.add_argument('--dev_dir', type=str, required=True,
                        help="""Output dev dir for prepared data""")
    parser.add_argument('--test_dir', type=str, required=True,
                        help="""Output test dir for prepared data""")
    parser.add_argument('--version', type=str, required=True,
                        help="""The version of CommonVoice dataset""")
    args = parser.parse_args()
    return args

def convert_num(text):
    converted_text = ' '
    for words in text.split():
        if re.search(r'\d', words):
            for word in words.split('-'):
                if len(word) > 50:
                    continue
                elif re.search(r'^\d{10,}$', word):
                    converted_text += p.number_to_words(word, group=1) + ' '
                elif re.search(r'^\d{2}[1-9]\dS?$', word):
                    converted_text += p.number_to_words(word, group=2) + ' '
                elif re.search(r'^\d{2}[1-9]0(?:\')?S$', word):
                    converted_text += p.number_to_words(word, group=2).replace('-', ' ') + ' S '
                elif re.search(r'^\d+\'S$', word):
                    converted_text += p.number_to_words(word).replace('-', ' ') + ' S '
                elif re.search(r'^\d+\'O$', word):
                    converted_text += p.number_to_words(word).replace('-', ' ') + ' O '
                elif re.search(r'^\d+(?:,\d{3})*(?:\.\d+)*$', word):
                    converted_text += p.number_to_words(word).replace('-', ' ') + ' '
                elif re.search(r'^\d+(?:,\d{3})*(ST|ND|RD|TH)$', word):
                    converted_text += p.number_to_words(word.lower()).replace('-', ' ') + ' '
                elif re.search(r'^\d+[^\d]+$', word):
                    converted_text += p.number_to_words(word).replace('-', ' ') + ' '
                    converted_text += re.sub(r'\d', '', word)+ ' '
                elif re.search(r'\d', word):
                    if len(word) < 10:
                        for char in word:
                            if ord(char) < 58:
                                converted_text += p.number_to_words(char) + ' '
                            else:
                                converted_text += char + ' '
                else:
                    converted_text += word + ' '
        else:
            converted_text += words + ' '
    converted_text = converted_text.replace(',', ' ')
    return converted_text.upper()

def process_num(m):
    text = re.sub(",","",m.group())
    text = num2words(int(text), lang="id")
    text = text.upper()
    return text

def text_proc(text):
    text = text.upper()

    ## non-ascii
    text = re.sub(r'[`‘’ʻʼ]', '\'', text)
    text = re.sub(r'–', '-', text)
    text = re.sub(r'[…，]', ',', text)

    ## notes
    text = re.sub(r' \(.*?\) | \[.*?\] | \{.*?\} ', ' ', text)
    text = re.sub(r' //\S* ', ' ', text)

    ## html tag
    text = re.sub(r'&GT;|&LT;|&LRM;|&RLM;', '', text)
    text = re.sub(r'&NBSP;', ' ', text)
    text = re.sub(r'&AMP;', ' DAN ', text)

    ## url
    text = re.sub(r' WWW\.(\w+)\.(COM|NET|EDU|ORG)/(\w+) ', r' WWW DOT \1 DOT \2 POTONG \3 ', text)
    text = re.sub(r' WWW\.(\w+)\.(COM|NET|EDU|ORG) ', r' WWW DOT \1 DOT \2 ', text)
    text = re.sub(r' (\w+)\.(COM|NET|EDU|ORG)/(\w+) ', r' \1 DOT \2 POTONG \3 ', text)
    text = re.sub(r' (\w+)\.(COM|NET|EDU|ORG) ', r' \1 DOT \2 ', text)

    ## email
    text = re.sub(r' (\w+)@(\w+)\.(COM|NET|EDU) ', r' \1 DI \2 DOT \3 ', text)
    
    ## money
    text = re.sub(r' \$(\d+)((?:,\d{3})*)((?:.\d+)*)( RIBUAN| JUTA| MILYAR)?([,.!?])? ', r' \1\2\3\4 DOLAR\5 ', text)
    text = re.sub(r' £(\d+)((?:,\d{3})*)((?:.\d+)*)( RIBUAN| JUTA| MILYAR)?([,.!?])? ', r' \1\2\3\4 POUND\5 ', text)
    text = re.sub(r' ¥(\d+)((?:,\d{3})*)((?:.\d+)*)( RIBUAN| JUTA| MILYAR)?([,.!?])? ', r' \1\2\3\4 YUAN\5 ', text)
    text = re.sub(r' €(\d+)((?:,\d{3})*)((?:.\d+)*)( RIBUAN| JUTA| MILYAR)?([,.!?])? ', r' \1\2\3\4 EURO\5 ', text)

    ## measurement
    text = re.sub(r' (\d+)% ', r' \1 PERSEN ', text)

    ## punct (reused from English)
    text = re.sub(r'(,){2,}|(\.){2,}|(!){2,}|(\?){2,}|(\-){2,}|(\'){2,}', r'\1\2\3\4\5\6 ', text)
    text = re.sub(r'([,.!?]){2,}', r'\1 ', text)
    text = re.sub(r'[:;"“”(){}\[\]<>#$%*+/=@\\^_~|`]', ' ', text)
    text = re.sub(r' \'+((?:[\w\-\']+[,.?!]*)+)\'+ ', r' \1 ', text)
    text = re.sub(r'([\w\'\- ]), ', r'\1 <KOMA> ', text)
    text = re.sub(r'([\w\'\- ])\. ', r'\1 <MASA> ', text)
    text = re.sub(r'([\w\'\- ])! ', r'\1 <TANDASERU> ', text)
    text = re.sub(r'([\w\'\- ])\? ', r'\1 <TANDATANYA> ', text)
    text = re.sub(r' \'+([\w\-\']+)\'+ ', r' \1 ', text)
    text = re.sub(r' \'+([\w\-\']+)((?: [\w\-\']+?)*)\'+ ', r' \1\2 ', text)
    text = re.sub(r' \'+BOUT ', ' ABOUT ', text)
    text = re.sub(r' \'+', ' ', text)

    ## number
    text = re.sub(r" '(\d)", r" \1", text)
    text = re.sub(r"\d+(,\d+)*",process_num,text)
    text = text.replace('--', ' ')
    text = re.sub(r'\s+', ' ', text)

    ## misc
    text = re.sub(r'é', "É", text)
    text = re.sub(r'É', "É", text)
    text = re.sub(r'°', " DERAJAT", text) 

    ## post
    text = re.sub(r'[,.?!]', ' ', text)
    text = re.sub(r'-+ [\-\']+| [\-\']+|-+ ', ' ', text)
    if re.search(r' \w(?:-\w)+ ', text):
        for group in re.findall(r' \w(?:-\w)+ ', text):
            text = text.replace(group, group.replace('-', ' '))
    text = re.sub(r' (?:UH) ', ' EH ', text) # according to google trans UH -> EH

    return text.strip()

def tsv_proc(tsv_path, wav_path, out_path, prefix):
    success = 0
    fail = 0
    skipped = 0

    with open(tsv_path) as f:
        lines = f.readlines()
    print(f"The number is {len(lines)-1}.")

    with open(f'{out_path}/wav.scp', 'w') as wavscp, \
         open(f'{out_path}/utt2spk', 'w') as utt2spk, \
         open(f'{out_path}/text', 'w') as utt2text:
        for line in lines[1:]:
            try:
                line = line.strip().split('\t')

                sid = f"{prefix}_"
                sid += line[0]
                uid = re.sub(r"(.*?).mp3", r"\1", line[1])
                utt2spk.write(f"{sid}_{uid} {sid}\n")

                wavscp.write(f"{sid}_{uid} sox {wav_path}/{line[1]} -r 16000 -c 1 -b 16 -e signed-integer -t wav - |\n")

                text = text_proc(line[2])
                utt2text.write(f"{sid}_{uid} {text}\n")

                success += 1
            except:
                fail += 1

    print(f"Succeeded: {success}, failed: {fail}, skipped: {skipped}.")

def run(in_path, train_path, dev_path, test_path, prefix, version):
    input_path = os.path.join(in_path, "id")
    wav_path = os.path.join(input_path, 'clips')
    print(train_path)
    print("Processing training set")
    tsv_path = os.path.join(input_path, 'train.tsv')
    tsv_proc(tsv_path, wav_path, train_path, prefix)

    print("Processing development set")
    tsv_path = os.path.join(input_path, 'dev.tsv')
    tsv_proc(tsv_path, wav_path, dev_path, prefix)

    print("Processing test set")
    tsv_path = os.path.join(input_path, 'test.tsv')
    tsv_proc(tsv_path, wav_path, test_path, prefix)


if __name__ == '__main__':
    args = get_args()

    run(
        args.input_dir,
        args.train_dir,
        args.dev_dir,
        args.test_dir,
        args.prefix,
        args.version,
    )
