import unittest
from utils import args as args_utils
from io import StringIO
from unittest.mock import patch

class ArgsTest(unittest.TestCase):
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

    def test_generate(self):
        args = args_utils.parse_args(['-g'])

        self.assertIsNotNone(args.generate)

    def test_query(self):
        args = args_utils.parse_args(['-q', '1'])

        self.assertIsNotNone(args.query)
        self.assertEqual(args.query, 1)

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
