
import sys
import re

START_PATTERN = re.compile(r'^(.*?)<ENAMEX$', re.I)
END_SINGLE_PATTERN = re.compile(r'^TYPE="(.*?)">(.*?)</ENAMEX>(.*?)$', re.I)
TYPE_PATTERN = re.compile(r'^TYPE="(.*?)">(.*?)$', re.I)
END_MULTI_PATTERN = re.compile(r'^(.*?)</ENAMEX>(.*?)$', re.I)
EOS_PATTERN = re.compile(r'^([^<>]*)\.?\t(\d+)$', re.I)
NON_ENTITY_TYPE = 'O'


def check_and_process_eos(token):
    match = re.match(EOS_PATTERN, token)
    if match:
        out.write(match.group(1) + '\t' + cur_type + '\n')
        out.write('.' + '\t' + cur_type + '\n')
        out.write('\n')
        return True
    return False


infile = sys.argv[1]
outfile = sys.argv[2]
cur_type = NON_ENTITY_TYPE
with open(infile, 'rb') as f, open(outfile, 'w') as out:
    for line in f:
        for token in line.strip().split(' '):
            token = token.strip()
            if not token:
                continue

            match = re.match(START_PATTERN, token)
            if match:
                if match.group(1):
                    out.write(match.group(1) + '\t' + NON_ENTITY_TYPE + '\n')
                continue

            match = re.match(END_SINGLE_PATTERN, token)
            if match:
                out.write(match.group(2) + '\t' + match.group(1) + '\n')
                cur_type = NON_ENTITY_TYPE
                if not check_and_process_eos(match.group(3)):
                    out.write(match.group(3) + '\t' + cur_type + '\n')
                continue

            match = re.match(TYPE_PATTERN, token)
            if match:
                cur_type = match.group(1)
                out.write(match.group(2) + '\t' + cur_type + '\n')
                continue

            match = re.match(END_MULTI_PATTERN, token)
            if match:
                out.write(match.group(1) + '\t' + cur_type + '\n')
                cur_type = NON_ENTITY_TYPE
                if not check_and_process_eos(match.group(2)):
                    out.write(match.group(2) + '\t' + cur_type + '\n')
                continue

            if check_and_process_eos(token):
                continue

            out.write(token + '\t' + cur_type + '\n')
