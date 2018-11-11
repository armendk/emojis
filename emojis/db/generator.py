import argparse
import os

import requests

JSON_DB_FILE = 'https://raw.githubusercontent.com/github/gemoji/master/db/emoji.json'

def generate(path, dbname):
    req = requests.get(JSON_DB_FILE)
    req.raise_for_status()

    data = req.json()

    path = os.path.join(path, dbname)

    with open(path, 'w') as file:
        file.write('### This is a generated file.\n')
        file.write('### Do not edit this file.\n')
        file.write('### This file is based on "{0}".\n'.format(JSON_DB_FILE))
        file.write('\n')
        file.write('from collections import namedtuple\n')
        file.write('\n')
        file.write('Emoji = namedtuple("Emoji", ["aliases", "emoji", "tags", "category"])\n')
        file.write('\n')
        file.write('EMOJI_DB = [\n')

        for emoji in data:
            if 'emoji' in emoji:
                file.write('    Emoji({aliases}, "{emoji}", {tags}, "{category}"),\n'.format(**{
                    'aliases': emoji['aliases'],
                    'emoji': emoji['emoji'],
                    'tags': emoji['tags'],
                    'category': emoji['category'],
                }))

        file.write(']\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates the Emoji database.')
    parser.add_argument('--dir', default='.', help='Database location')
    parser.add_argument('--dbname', default='db.py', help='Database location')
    args = parser.parse_args()

    generate(args.dir, args.dbname)
