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

    #we test our exceptions.
    def test_exchange(self):
        #assuming getRate test works, we pay the exact amount plus the fee cost to spend the whole of a base currency
        #1000/1.03 is the amount minus the 3% charged for any given currency
        amountToExchange = getRate("USD","CAD",1000/1.0300001)
        #print(amountToExchange)
        #print(getRate("CAD","USD",1213.5922330097087))

        #buying the exact amount of CAD for 970 USD should give us a USD balance of 0
        exchange("USD","CAD",amountToExchange)
        self.assertAlmostEqual(currentBalance["USD"], 0, places=3)

        #if our getFeeCost passed, we use it to calculate what we expect
        with self.assertRaises(ValueError):
            exchange("NZD", "EUR", 100)
            exchange("EUR", "GBP", 2000)
            #We regression test by exhausting a currency's balance.
            exchange("USD","CAD",1)

    #def test_calculateTotalFees():
        #pass

if __name__ == '__main__':
    unittest.main()
