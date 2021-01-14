#!env python3

from pathlib import Path
from time import sleep

from .fetcher import fetch_definitions

from interutils import pr, choose
from requests import RequestException


def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-d', '--defs', nargs='+',
                        help="Specify custom definitions")
    parser.add_argument('-f', '--file', help="Load definitions from file")
    parser.add_argument('-c', '--columns', nargs='+', help="Columns to show")
    parser.add_argument('-i', '--interactive',
                        action='store_true', help="Interactive menu mode")
    parser.add_argument('-a', '--automode', action='store_true',
                        help="Automatically reload and show")
    parser.add_argument('-at', '--automode-time', type=int, default=5,
                        help="Time to sleep between refreshes in seconds for automode")
    parser.add_argument('-nc', '--no-color', action='store_true',
                        help="Print no colors in the table")
    parser.add_argument('--clear', action='store_true',
                        help="Whether to clear screen begore showing data")
    parser.add_argument('--no-table', action='store_true',
                        help="Print format in ASCII table")
    parser.add_argument('--nt-no-header', action='store_true',
                        help="Don't print a header with no-table mode")
    parser.add_argument('--nt-delimiter', default='\t',
                        help="Delimiter to use with no-table mode")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Minimal output")
    return parser.parse_args()


def _check_def(d):
    if ' ' not in d:
        return False
    if d.count(' ') > 1:
        return False
    return True


def menu(args, definitions) -> int:
    auto_mode = args.automode
    auto_time = min(0.1, args.automode_time)
    while 1:
        try:
            fetch_definitions(args, definitions)
            if auto_mode:
                sleep(auto_time)
        except KeyboardInterrupt:
            print()
            if auto_mode:
                auto_mode = False
                if not args.quiet:
                    pr('Auto-mode stopped!')
            else:
                if not args.quiet:
                    pr('Interrupted!', '!')
                break
        except RequestException:
            pr("Couldn't connect to API @ api.cryptowat.ch", 'X')
            return 2

        if not auto_mode:
            c = choose(['Reload values', 'Enter auto mode'])
            if c == 0:
                continue
            elif c == 1:
                auto_mode = True
            else:
                break
    if not args.quiet:
        pr('Bye!')


def main() -> int:
    args = parse_args()

    definitions = []
    if args.file:
        file = Path(args.file)
        if not file.is_file():
            pr('Specified file not found!', '!')
        else:
            definitions = file.read_text().splitlines()
            for d in definitions:
                if not _check_def(d):
                    pr(f'Suspicious definition: "{d}" from file', '!')
    if args.defs:
        if len(args.defs) == 1 and ',' in args.defs[0]:
            args.defs = args.defs[0].split(',')

        definitions += args.defs
        for d in args.defs:
            if not _check_def(d):
                pr(f'Suspicious definition: "{d}" from arguments', '!')

    if not definitions:
        pr('No definitions defined, exiting', '!')
        exit(1)

    if args.interactive or args.automode:
        return menu(args, definitions)

    return fetch_definitions(args, definitions)


if __name__ == "__main__":
    exit(main())
