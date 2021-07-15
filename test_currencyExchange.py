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

        #buying the exact amount of CAD for 1000/1.03 USD should give us a USD balance of 0
        exchange("USD","CAD",amountToExchange)
        self.assertAlmostEqual(currentBalance["USD"], 0, places=3)

        #we evaluate the cases where an error should be raised
        with self.assertRaises(ValueError):
            exchange("NZD", "NZD", 100)
            exchange("EUR", "GBP", 2000)
            #We regression test by exhausting a currency's balance. Since we spent all our USD, we should'nt be able to buy anything with it.
            exchange("USD","CAD",1)

    #def test_calculateTotalFees(self):
        ##since we made a transaction in our past tests and assuming it's the only one registered in the database, we know the aproximate
        ##amount that should've been charged. About 3% of 1000.
        #totalFees = calculateTotalFees()
        #print(str(totalFees))
        #self.assertAlmostEqual(totalFees,30, places=1)

if __name__ == '__main__':
    unittest.main()
