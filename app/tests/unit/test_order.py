import mock
import unittest

from app.models.order import Status, Order, Table


class MealsEntityTest(unittest.TestCase):

    def test_table_str_method_should_return_table_name(self):
        table_name = "Example table name"

        mock_instance = mock.Mock(spec=Table)
        mock_instance.name = table_name

        self.assertEqual(Table.__str__(mock_instance), table_name)

    def test_status_str_method_should_return_status_name(self):
        status_name = "Example status name"

        mock_instance = mock.Mock(spec=Status)
        mock_instance.name = status_name

        self.assertEqual(Status.__str__(mock_instance), status_name)

