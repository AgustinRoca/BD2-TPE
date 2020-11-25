import unittest
from utils import args as args_utils
from io import StringIO
from unittest.mock import patch


class PostgresArgsTest(unittest.TestCase):
    def test_postgres_config(self):
        args = args_utils.parse_args([
            '-g',
            '-ph', 'host',
            '-pp', '5432',
            '-pd', 'database',
            '-pU', 'username',
            '-pP', 'password'
        ])

        self.assertIsNotNone(args.ph)
        self.assertIsNotNone(args.pp)
        self.assertIsNotNone(args.pd)
        self.assertIsNotNone(args.pU)
        self.assertIsNotNone(args.pP)

        config = args_utils.get_postgres_config(args)

        self.assertEqual(config['host'], 'host')
        self.assertEqual(config['port'], '5432')
        self.assertEqual(config['database'], 'database')
        self.assertEqual(config['username'], 'username')
        self.assertEqual(config['password'], 'password')

    @patch('sys.stderr', new_callable=StringIO)
    def test_postgres_config_invalid_port_type(self, mock_stderr):
        with self.assertRaises(ValueError):
            args_utils.parse_args([
                '-g',
                '-ph', 'host',
                '-pp', 'as',
                '-pd', 'database',
                '-pU', 'username',
                '-pP', 'password'
            ])

    def test_postgres_config_port_too_small(self):
        with self.assertRaises(ValueError):
            args_utils.parse_args([
                '-g',
                '-ph', 'host',
                '-pp', '-1',
                '-pd', 'database',
                '-pU', 'username',
                '-pP', 'password'
            ])

    def test_postgres_config_port_too_big(self):
        with self.assertRaises(ValueError):
            args_utils.parse_args([
                '-g',
                '-ph', 'host',
                '-pp', str(0xFFFF + 1),
                '-pd', 'database',
                '-pU', 'username',
                '-pP', 'password'
            ])

    def test_postgres_config_max_port(self):
        try:
            args_utils.parse_args([
                '-g',
                '-ph', 'host',
                '-pp', str(0xFFFF),
                '-pd', 'database',
                '-pU', 'username',
                '-pP', 'password'
            ])
        except ValueError:
            self.fail('Shouldn\'t raise error')

    def test_postgres_config_min_port(self):
        try:
            args_utils.parse_args([
                '-g',
                '-ph', 'host',
                '-pp', '0',
                '-pd', 'database',
                '-pU', 'username',
                '-pP', 'password'
            ])
        except ValueError:
            self.fail('Shouldn\'t raise error')


class RedisTest(unittest.TestCase):
    def test_redis_config(self):
        args = args_utils.parse_args([
            '-g',
            '-rh', 'host',
            '-rp', '6399',
            '-rd', '0'
        ])

        self.assertIsNotNone(args.rh)
        self.assertIsNotNone(args.rp)
        self.assertIsNotNone(args.rd)

        config = args_utils.get_redis_config(args)

        self.assertEqual(config['host'], 'host')
        self.assertEqual(config['port'], 6399)
        self.assertEqual(config['database'], 0)

    @patch('sys.stderr', new_callable=StringIO)
    def test_redis_config_invalid_port_type(self, mock_stderr):
        with self.assertRaises(SystemExit):
            args_utils.parse_args([
                '-g',
                '-rh', 'host',
                '-rp', 'port',
                '-rd', '0'
            ])
        self.assertRegexpMatches(mock_stderr.getvalue(), r"error.*invalid int value")

    @patch('sys.stderr', new_callable=StringIO)
    def test_redis_config_invalid_database_type(self, mock_stderr):
        with self.assertRaises(SystemExit):
            args_utils.parse_args([
                '-g',
                '-rh', 'host',
                '-rp', '0',
                '-rd', 'database'
            ])
        self.assertRegexpMatches(mock_stderr.getvalue(), r"error.*invalid int value")

    def test_redis_config_port_too_small(self):
        with self.assertRaises(ValueError):
            args_utils.parse_args([
                '-g',
                '-rh', 'host',
                '-rp', '-1',
                '-rd', '0'
            ])

    def test_redis_config_port_too_big(self):
        with self.assertRaises(ValueError):
            args_utils.parse_args([
                '-g',
                '-rh', 'host',
                '-rp', str(0xFFFF + 1),
                '-rd', '0'
            ])

    def test_redis_config_max_port(self):
        try:
            args_utils.parse_args([
                '-g',
                '-rh', 'host',
                '-rp', str(0xFFFF),
                '-rd', '0'
            ])
        except ValueError:
            self.fail('Shouldn\'t raise error')

    def test_redis_config_min_port(self):
        try:
            args_utils.parse_args([
                '-g',
                '-rh', 'host',
                '-rp', '0',
                '-rd', '0'
            ])
        except ValueError:
            self.fail('Shouldn\'t raise error')


class ArgsTest(unittest.TestCase):
    def test_generate(self):
        args = args_utils.parse_args(['-g'])

        self.assertIsNotNone(args.generate)

    def test_query(self):
        args = args_utils.parse_args(['-q', '1'])

        self.assertIsNotNone(args.query)
        self.assertEqual(args.query, 1)

    @patch('sys.stderr', new_callable=StringIO)
    def test_invalid_query(self, mock_stderr):
        with self.assertRaises(SystemExit):
            args_utils.parse_args(['-q', 'a'])
        self.assertRegexpMatches(mock_stderr.getvalue(), r"error.*invalid int value")

    @patch('sys.stderr', new_callable=StringIO)
    def test_no_args(self, mock_stderr):
        with self.assertRaises(SystemExit):
            args_utils.parse_args([])
        self.assertRegexpMatches(mock_stderr.getvalue(), r"error.*argument.*required")

    @patch('sys.stderr', new_callable=StringIO)
    def test_generate_query_args(self, mock_stderr):
        with self.assertRaises(SystemExit):
            args_utils.parse_args(['-g', '-q', '1'])
        self.assertRegexpMatches(mock_stderr.getvalue(), r"error.*argument.*not allowed")
