import unittest
from currencyExchange import *

class TestCurrencyExchange(unittest.TestCase):
    #Since we used in our dataset the USD as base currency, we check we're getting the same amount of CAD for 1 USD
    def test_getRate(self):
        result = getRate("USD", "CAD", 1)
        self.assertEqual(result, 1.25)

    def test_getFeeCost(self):
        result = getFeeCost(1)
        self.assertEqual(1*0.03)


if __name__ == '__main__':
    unittest.main()
