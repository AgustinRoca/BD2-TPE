import argparse
from utils import database_connections as dbc


def parse_args(args):
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Main program for BD2 TPE")
    group = parser.add_mutually_exclusive_group(required=True)

    # add arguments
    parser.add_argument('-ph', '--postgres-host', dest='ph',
                        help='Specifies the postgres DB host url. Default: "127.0.0.1"')
    parser.add_argument('-pp', '--postgres-port', dest='pp',
                        help='Specifies the postgres DB port. Default: "5432"')
    parser.add_argument('-pd', '--postgres-database', dest='pd',
                        help='Specifies the postgres DB. Default: "postgres"')
    parser.add_argument('-pU', '--postgres-username', dest='pU',
                        help='Specifies the postgres DB username. Default: "postgres"')
    parser.add_argument('-pP', '--postgres-password', dest='pP',
                        help='Specifies the postgres DB password. Default: "password"')

    parser.add_argument('-rh', '--redis-host', dest='rh', help='Specifies the redis DB host url. Default: "localhost"')
    parser.add_argument('-rp', '--redis-port', dest='rp', type=int, help='Specifies the redis DB port. Default: "6379"')
    parser.add_argument('-rd', '--redis-database', dest='rd', type=int, help='Specifies the redis DB. Default: "0"')

    group.add_argument('-q', '--query', dest='query', type=int, help='Specifies the query to run')
    group.add_argument('-g', '--generate', dest='generate', action='store_true', help='Populates databases')

    args = parser.parse_known_args(args)[0]
    _assert_port(args.pp)
    _assert_port(args.rp)
    return args


def set_config(arg, config: dict, key: str):
    if isinstance(arg, int) or (isinstance(arg, str) and len(arg) > 0):
        config[key] = arg


def get_postgres_config(args: argparse.Namespace):
    config = dbc.PostgresConnection.DEFAULT_CONFIG.copy()

    if args.pp is not None:
        pp = str(args.pp)
    else:
        pp = None

    set_config(args.ph, config, 'host')
    set_config(pp, config, 'port')
    set_config(args.pd, config, 'database')
    set_config(args.pU, config, 'username')
    set_config(args.pP, config, 'password')

    return config


def get_redis_config(args: argparse.Namespace):
    config = dbc.RedisConnection.DEFAULT_CONFIG.copy()

    if args.rp is not None:
        rp = int(args.rp)
    else:
        rp = None

    if args.rd is not None:
        rd = int(args.rd)
    else:
        rd = None

    set_config(args.rh, config, 'host')
    set_config(rp, config, 'port')
    set_config(rd, config, 'database')

    return config


def _assert_port(port):
    if port is None:
        return

    if isinstance(port, str):
        port = int(port)
    if port < 0 or 0xFFFF < port:
        raise ValueError('Port number out of bounds')
