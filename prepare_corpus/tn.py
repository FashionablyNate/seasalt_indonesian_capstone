import re
import os
import sys

import webvtt
import librosa
import inflect
from unidecode import unidecode


startname = 'YouTube'
wavoutput_file = 'wav.scp_tn'
spkoutput_file = 'spk2utt_tn'
uttoutput_file = 'utt2spk_tn'
text_file = 'text_tn'
segment_file = 'segments_tn'
wavdir = sys.argv[1]
vttdir = sys.argv[2]
p = inflect.engine()


def convert_num(text):
    converted_text = ' '
    for words in text.split():
        if re.search(r'\d', words):
            for word in words.split('-'):
                if len(word) > 50:
                    continue
                elif re.search(r'^\d{10,}$', word):
                    converted_text += p.number_to_words(word, group=1) + ' '
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

def filter_words(text):
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
    text = re.sub(r'&AMP;', ' AND ', text)
    ## url
    text = re.sub(r' WWW\.(\w+)\.(COM|NET|EDU|ORG)/(\w+) ', r' WWW DOT \1 DOT \2 SLASH \3 ', text)
    text = re.sub(r' WWW\.(\w+)\.(COM|NET|EDU|ORG) ', r' WWW DOT \1 DOT \2 ', text)
    text = re.sub(r' (\w+)\.(COM|NET|EDU|ORG)/(\w+) ', r' \1 DOT \2 SLASH \3 ', text)
    text = re.sub(r' (\w+)\.(COM|NET|EDU|ORG) ', r' \1 DOT \2 ', text)
    ## email
    text = re.sub(r' (\w+)@(\w+)\.(COM|NET|EDU) ', r' \1 AT \2 DOT \3 ', text)
    ## money
    text = re.sub(r' \$(\d+)((?:,\d{3})*)((?:.\d+)*)( THOUSAND| MILLION| BILLION)?([,.!?])? ', r' \1\2\3\4 DOLLARS\5 ', text)
    text = re.sub(r' £(\d+)((?:,\d{3})*)((?:.\d+)*)( THOUSAND| MILLION| BILLION)?([,.!?])? ', r' \1\2\3\4 POUNDS\5 ', text)
    text = re.sub(r' ¥(\d+)((?:,\d{3})*)((?:.\d+)*)( THOUSAND| MILLION| BILLION)?([,.!?])? ', r' \1\2\3\4 YUAN\5 ', text)
    text = re.sub(r' €(\d+)((?:,\d{3})*)((?:.\d+)*)( THOUSAND| MILLION| BILLION)?([,.!?])? ', r' \1\2\3\4 EUROS\5 ', text)
    ## time
    text = re.sub(r' (\d{1,2})(AM|PM) ', r' \1 \2 ', text)
    ## measurement
    text = re.sub(r' (\d+)% ', r' \1 PERCENT ', text)
    ## non-ascii
    text = unidecode(text)
    text = text.upper()
    ## punct
    text = re.sub(r'(,){2,}|(\.){2,}|(!){2,}|(\?){2,}|(\-){2,}|(\'){2,}', r'\1\2\3\4\5\6 ', text)
    text = re.sub(r'([,.!?]){2,}', r'\1 ', text)
    text = re.sub(r'[:;"“”(){}\[\]<>#$%*+/=@\\^_~|`]', ' ', text)
    text = re.sub(r' \'+((?:[\w\-\']+[,.?!]*)+)\'+ ', r' \1 ', text)
    text = re.sub(r'([\w\'\- ]), ', r'\1 <COMMA> ', text)
    text = re.sub(r'([\w\'\- ])\. ', r'\1 <PERIOD> ', text)
    text = re.sub(r'([\w\'\- ])! ', r'\1 <EXCLAMATIONPOINT> ', text)
    text = re.sub(r'([\w\'\- ])\? ', r'\1 <QUESTIONMARK> ', text)
    text = re.sub(r' \'+([\w\-\']+)\'+ ', r' \1 ', text)
    text = re.sub(r' \'+([\w\-\']+)((?: [\w\-\']+?)*)\'+ ', r' \1\2 ', text)
    text = re.sub(r' \'+BOUT ', ' ABOUT ', text)
    # text = re.sub(r'IN\'+ ', 'ING ', text)
    text = re.sub(r' \'+', ' ', text)
    ## number
    text = convert_num(text)
    ## post
    # text = text.encode('ascii', 'ignore').decode()
    text = re.sub(r'[,.?!]', ' ', text)
    text = re.sub(r'-+ [\-\']+| [\-\']+|-+ ', ' ', text)
    if re.search(r' \w(?:-\w)+ ', text):
        for group in re.findall(r' \w(?:-\w)+ ', text):
            text = text.replace(group, group.replace('-', ' '))
    # text = re.sub(r'<COMMA>|<PERIOD>|<EXCLAMATIONPOINT>|<QUESTIONMARK>', ' ', text)
    ## UH EH -> AH
    text = re.sub(r' (?:UH|EH) ', ' AH ', text)

    text = re.sub(r'\s+', ' ', text)

    return text

if __name__ == '__main__':
    exclude = {}

    # TODO: findout what this does
    """
    with open('stream') as f:
        lines = f.readlines()
    with open('punct') as f:
        lines += f.readlines()
    with open('not_ascii') as f:
        lines += f.readlines()
    with open('test') as f:
        lines += f.readlines()
    with open('duplicate') as f:
        lines += f.readlines()
    for line in lines:
        exclude[line.strip()] = 0
    """

    dict = {}
    parse_json_files = []
    names = []
    for root, dirs, files in os.walk(wavdir):
        for f in files:
            filename = str(f)
            if filename.endswith('.opus'):
                
                #name = f.split('.')[0]
                name = f.replace(".opus","")[-11:]
                name = f"yt_en_{name}"
                print(name)
                if name not in exclude:
                    names.append(name)
                    dict[name] = name
                    parse_json_files.append(os.path.join(root, f))
    with open(wavoutput_file, "w") as file:
        for i in range(len(names)):
            # file.write(f'{names[i]} {parse_json_files[i]}\n')
            file.write(f'{names[i]} ffmpeg -i {parse_json_files[i]} -f wav -ar 16000 -ac 1 - |\n')

    text_content = []
    seg_content = []
    spk_content = []

    already_seen = set()
    for root, dirs, files in os.walk(vttdir):
        for f in files:
            filename = str(f)

            if filename.endswith('.vtt'):
                parse_json_file = os.path.join(root, f)
                #file_name = f.split('.')[0]
                file_name = f.replace(".en-US","").replace(".en","").replace(".vtt","")[-11:]
                file_name = f"yt_en_{file_name}"
                print(file_name)
                try:
                    name = dict[file_name]
                    if file_name in already_seen:
                        print("Duplicate file, skipping")
                        continue
                    already_seen.add(file_name)
                except KeyError:
                    print("Failed with dict[file_name]")
                    continue
                if os.path.getsize(parse_json_file) != 0:
                    try:
                        filename = filename.replace(".en-US","").replace(".en","")
                        end = librosa.get_duration(filename=f'{os.path.join(wavdir,filename[:-3])}opus')
                    except FileNotFoundError:
                        print(f"Couldn't find audio for {os.path.join(wavdir,filename[:-3])}opus") 
                        continue

                    text = ' '
                    try:
                        for caption in webvtt.read(parse_json_file):
                            text += ' '.join(caption.text.split('\n')) + ' '
                        text = filter_words(text)
                         
                        if text != '' and end != 0:
                            seg_content.append(f'{name} {name} 0 {end}\n')
                            spk_content.append(f'{name} {name}\n')
                            text_content.append(f'{name} {text.strip()}\n')
                    except Exception as e:
                        print(f"{e}: Ill-formed vtt for {filename}")

    with open(text_file, 'w') as f:
        text_content = ''.join(text_content)
        f.write(text_content)
    with open(segment_file, 'w') as f:
        seg_content = ''.join(seg_content)
        f.write(seg_content)
    with open(spkoutput_file, 'w') as f:
        spk_content = ''.join(spk_content)
        f.write(spk_content)
    with open(uttoutput_file, 'w') as f:
        spk_content = ''.join(spk_content)
        f.write(spk_content)
