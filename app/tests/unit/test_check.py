import mock
import unittest

from app.models.check import ServicePercentage


class CheckEntityTest(unittest.TestCase):

    def test_percentage_str_method_should_return_percentage_sum(self):
        percentage_sum = 30

        mock_instance = mock.Mock(spec=ServicePercentage)
        mock_instance.percentage = percentage_sum

        self.assertEqual(ServicePercentage.__str__(mock_instance), percentage_sum)
