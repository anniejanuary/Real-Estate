"""
Test for Django custom commands.
"""
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2Error


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """
    Test commands.
    Mocking command in patch decorator in order to fake the db response.

    Args:
        SimpleTestCase: no test database created because of that inheritance.
    """

    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for database command - if database ready for connection.
        """
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test databse waiting when getting OperationalError or Psycopg2Error.

        Args:
            patched_sleep: mock for time module method
            patched_check: mock for check method from Command django module
        """
        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
