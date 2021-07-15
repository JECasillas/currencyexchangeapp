import unittest
from currencyExchange import *

class TestCurrencyExchange(unittest.TestCase):
    #Since we used in our dataset the USD as base currency, we check we're getting the same amount of CAD for 1 USD
    def test_getRate(self):
        result = getRate("USD", "CAD", 1)
        self.assertEqual(result, 1.25)

    #we merely test our 3% set
    def test_getFeeCost(self):
        result = getFeeCost(1)
        self.assertEqual(result, 1*0.03)

    def test_exchange(self):
        #result = exchange("USD", "CAD", 100)
        #if our getFeeCost passed, we use it to calculate what we expect
        with self.assertRaises(ValueError):
            exchange("USD", "USD", 100)
            exchange("USD", "GBP", 2000)

    #def test_calculateTotalFees():
        #pass

if __name__ == '__main__':
    unittest.main()
