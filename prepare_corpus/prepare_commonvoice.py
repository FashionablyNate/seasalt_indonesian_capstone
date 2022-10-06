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
    text = re.sub(",","",m)
    text = num2words(text, lang="fr")
    return text

#    text = re.sub(r'â', "â", text)
#    text = re.sub(r'ä', "a", text)
#    text = re.sub(r'ã', "a", text)
#    text = re.sub(r'á', "á", text)
#    text = re.sub(r'é', "é", text)
#    text = re.sub(r'è', "è", text)
#    text = re.sub(r'ê', "ê", text)
#    text = re.sub(r'î', "î", text)
#    text = re.sub(r'Ç', "ç", text)
#    text = re.sub(r'ç', "ç", text)
#    text = re.sub(r'õ', "o", text)
#    text = re.sub(r'ō', "o", text)
#    text = re.sub(r'ū', "u", text)
#    text = re.sub(r'ß', "s", text)
def text_proc(text):
    text = text.lower()
    text = re.sub(r"[\-,\.!\?\"{};:.,\(\)…ʿ“”=]", '', text)
    text = re.sub(r"[’`′´]", "'", text)
    text = re.sub(r"[|]", ' ', text)
    text = re.sub(r' – ', " ", text)
    text = re.sub(r'–', " ", text)
    text = re.sub(r'[-_]', " ", text)
    #text = re.sub(fr'{decode_hex("\xa0")[0]}', " ", text)
    #text = re.sub(r'œ', "oe", text)
    #text = re.sub(r'°', " degrés", text)
    text = re.sub(r'æ', "ae", text)
    text = re.sub(r'â', "â", text)
    text = re.sub(r'ã', "a", text)
    text = re.sub(r'ā', "a", text)
    text = re.sub(r'á', "á", text)
    text = re.sub(r'à', "à", text)
    text = re.sub(r'é', "é", text)
    text = re.sub(r'É', "é", text)
    text = re.sub(r'è', "è", text)
    text = re.sub(r'ê', "ê", text)
    text = re.sub(r'ě', "e", text)
    text = re.sub(r'ę', "e", text)
    text = re.sub(r'ī', "i", text)
    text = re.sub(r'í', "i", text)
    text = re.sub(r'ı', "i", text)
    text = re.sub(r'î', "î", text)
    text = re.sub(r'č', "c", text)
    text = re.sub(r'ć', "c", text)
    text = re.sub(r'ċ', "c", text)
    text = re.sub(r'Ç', "ç", text)
    text = re.sub(r'ç', "ç", text)
    text = re.sub(r'ň', "n", text)
    text = re.sub(r'ń', "n", text)
    text = re.sub(r'õ', "o", text)
    text = re.sub(r'ō', "o", text)
    text = re.sub(r'ø', "o", text)
    text = re.sub(r'ô', "ô", text)
    text = re.sub(r'ū', "u", text)
    text = re.sub(r'ů', "u", text)
    text = re.sub(r'ù', "ù", text)
    text = re.sub(r'û', "û", text)
    text = re.sub(r'ß', "s", text)
    text = re.sub(r'ł', "l", text)
    text = re.sub(r'š', "s", text)
    text = re.sub(r'ș', "s", text)
    text = re.sub(r'ş', "s", text)
    text = re.sub(r'ț', "t", text)
    text = re.sub(r'ÿ', "y", text)
    text = re.sub(r'ż', "z", text)
    text = re.sub(r'ž', "z", text)
    text = re.sub(r'°', " degrés", text)
    text = re.sub(r' encor ', " encore ", text)
    text = re.sub(r' mâtin ', " matin ", text)
    text = re.sub(r' plangô ', " plango ", text)
    text = re.sub(r' premiere ', " première ", text)
    text = re.sub(r' pére ', " père ", text)
    text = re.sub(r' quarant ', " quarante ", text)
    text = re.sub(r' qutre ', " quatre ", text)
    text = re.sub(r' rhythme ', " rythme ", text)
    text = re.sub(r' rhythmées ', " rythmées ", text)
    text = re.sub(r' shiraz ', " schiraz ", text)
    text = re.sub(r' sixème ', " sixième ", text)
    text = re.sub(r' tems ', " temps ", text)
    text = re.sub(r' égypte ', " egypte ", text)
    text = re.sub(r' m ', " monsieur ", text)
    text = re.sub(r' mm ', " messieurs ", text)
    text = re.sub(r' mr ', " monsieur ", text)
    text = re.sub(r' mosieu ', " monsieur ", text)
    text = re.sub(r' mme ', " madame ", text)
    text = re.sub(r' mlle ', " mademoiselle ", text)
    text = re.sub(r" '(\d)", r" \1", text)
    text = re.sub(r"\d+(,\d+)*",process_num,text)
    text = text.replace('--', ' ')
    text = re.sub(r'\s+', ' ', text)
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
