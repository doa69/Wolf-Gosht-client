
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
import sqlalchemy as db
from pprint import pprint

engine = db.create_engine('postgresql://postgres:postgres@localhost/dvdrental')
connection = engine.connect()

query = db.sql.text("""select actor.actor_id, actor.first_name, actor.last_name, x.cooccurrence from (
    select film_actor2.actor_id, count(*) as cooccurrence
    from film_actor film_actor1 join film_actor film_actor2 on film_actor1.film_id = film_actor2.film_id
    where film_actor1.actor_id != film_actor2.actor_id 
    and film_actor1.actor_id = :actor_id
    group by film_actor1.actor_id, film_actor2.actor_id
) x join actor on x.actor_id = actor.actor_id
where x.cooccurrence > 2
order by x.cooccurrence desc
""")


input_actor_id = 107
result = connection.execute(query, actor_id=input_actor_id).fetchall()
pprint(result)
