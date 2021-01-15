
from json import loads
from subprocess import call
from time import strftime

from interutils import pr
from prettytable import PrettyTable
from requests import get, Response
from termcolor import colored, cprint


API_USAGE_CAP = 10


def _cval(val: float, colorize: bool, suffix: str = '') -> str:
    col = None
    if colorize:
        if val > 0:
            col = 'green'
        elif val < 0:
            col = 'red'
    s = '%.3f%s' % (val, suffix)
    if not col:
        return s
    return colored(s, col)


def _api_request(market, pair) -> (dict, None):
    pair = pair.replace('/', '').replace('\\', '')

    resp = None
    try:
        resp = get(
            f'https://api.cryptowat.ch/markets/{market.lower()}/{pair.lower()}/summary')
        if resp.status_code == 200:
            return loads(resp.text)  # json

        if resp.status_code == 429:
            pr(f'API is depleted! renewal in {60 - int(strftime(" % M"))} minutes', '!')
        elif resp.status_code == 404:
            pr(f'Pair "{pair}" in "{market}" not found!', 'X')
        else:
            pr('Received bad code from the server: %d' %
                resp.status_code, 'X')
        return None
    finally:
        if type(resp) == Response:
            resp.close()


def fetch_definitions(args, definitions: iter):

    # Get data
    api_usage = api_fetch_cost = 0
    if not args.quiet:
        pr(f'Downloading {colored(len(definitions), "cyan")} cryptos..')
        pr('Timestamp: ' + strftime('%Y-%m-%d %H:%M:%S'))

    table = []
    for definition in definitions:
        market, pair = definition.split()

        json = _api_request(market, pair)
        api_usage = json['allowance']['remaining']  # / API_USAGE_CAP
        api_fetch_cost += json['allowance']['cost']  # / API_USAGE_CAP
        price = json['result']['price']

        colorize = not args.no_color
        if colorize:
            pair = colored(pair, 'cyan')

        table.append((
            market, pair, price['last'],
            price['low'], price['high'],
            _cval(float(price['change']['absolute']), colorize),
            _cval(float(price['change']['percentage']) * 100.0, colorize, suffix='%')))

    if args.clear or args.interactive:
        call('clear')

    if not args.quiet:
        pr('Fetch finished: API usage: %.3f, Last fetch cost: %.3f' %
           (api_usage, api_fetch_cost))

    # Show data based on args
    header = ('Market', 'Pair', 'Current', 'Lowest',
              'Highest', 'Absolute', 'Percentage')

    selected = []  # List of selected columns indexes
    if args.columns:
        # Expand nargs in case they passed like: `a,b,c` instead of `a b c`
        if len(args.columns) == 1 and ',' in args.columns[0]:
            args.columns = args.columns[0].split(',')

        for col in args.columns:
            col = col.capitalize()
            if col not in header:
                pr('Invalid column specified: ' + col, 'X')
                exit()
            selected.append(header.index(col))

    def _filter_selected_columns(lst: list) -> list:
        if not selected:
            return lst
        return [str(k) for k in lst if lst.index(k) in selected]

    # Print data in requested format
    if not args.no_table:
        pt = PrettyTable(_filter_selected_columns(header))
        for row in table:
            pt.add_row(_filter_selected_columns(row))
    else:
        pt = []
        if not args.nt_no_header:
            table.insert(0, header)
        delim = args.nt_delimiter
        for row in table:
            pt.append(delim.join(_filter_selected_columns(row)))
        pt = '\n'.join(pt)
    print(pt)
