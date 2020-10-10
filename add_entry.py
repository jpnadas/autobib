import biblib.bib
import argparse
import sys


def get_new_entry_key(db, entry):
    entry.key = entry.key.replace('_', '')

    if entry.key.lower() in db:
        existing_entry = db.get(entry.key.lower())
        if entry.get('title') == existing_entry.get('title'):
            print("nothing to do, entry already in the database")
            return None
        else:
            entry.key += 'a'
            return get_new_entry_key(db, entry)
    else:
        return entry.key

def main():
    arg_parser = argparse.ArgumentParser(
        description='Flatten macros, combine, and pretty-print .bib database(s)')
    arg_parser.add_argument('bib', nargs='+', help='.bib file(s) to process',
                            type=open)
    arg_parser.add_argument('add', nargs='+', help='entry to add',
                            type=open)
    args = arg_parser.parse_args()

    original_bib = args.bib[0].name

    try:
        # Load databases
        db = biblib.bib.Parser().parse(args.bib, log_fp=sys.stderr).get_entries()
    except biblib.messages.InputError:
        sys.exit(1)

    try:
        # Load databases
        new_db = biblib.bib.Parser().parse(args.add, log_fp=sys.stderr).get_entries()
    except biblib.messages.InputError:
        sys.exit(1)

    for ent in new_db.values():
        ent.key = get_new_entry_key(db, ent)
        if ent.key is not None:
            with open(original_bib, 'a') as fil:
                ent.pop('url')
                fil.write(f"\n{ent.to_bib()}")
                print(ent.to_bib())

if __name__ == '__main__':
    main()
