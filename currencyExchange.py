import json
from datetime import datetime

#WE USE USD AS BASE REFERENCE FOR ALL OTHER CURRENCIES
currencyRates = {"USD": 1,
"GBP": 0.72,
"EUR": 0.84,
"JPY": 110.10,
"CHF": 0.91,
"AUD": 1.34,
"CAD": 1.25,
"NZD": 1.44
}

currentBalance = {"USD": 1000,
"GBP": 1000,
"EUR": 1000,
"JPY": 1000,
"CHF": 1000,
"AUD": 1000,
"CAD": 1000,
"NZD": 1000
}

#We will define the fee as 3% of every transaction
feePercentage = 3

#We're using a json file as our local database for our fees registries
feesRegistry = open("feesregistries.json", "r")
feesDict = json.load(feesRegistry)
feesRegistry.close()


##
# Gets the rate for two currencies
# @param  {string}   baseCurrency           the base currency of the rate
# @param  {string}   quoteCurrency          the quote currency of the rate
# @param  {float}    baseCurrencyAmount     the amount the user wants to know the exchange of
# @return {float}    the exchange rate amount
##
def getRate(baseCurrency, quoteCurrency, baseCurrencyAmount):
    rate = currencyRates[quoteCurrency]/currencyRates[baseCurrency]
    exchangeRate = rate*baseCurrencyAmount
    return exchangeRate

##
# Calculates the fee or cost for a specified amount in the base currency
# @param  {string}   baseCurrency           the base currency of the rate
# @param  {float}    baseCurrencyAmount     the amount the user wants to know the exchange of
# @return {float}    the calculated fee in the base currency
##
def getFeeCost(baseCurrency, baseCurrencyAmount):
    #return str((feePercentage/100)*baseCurrencyAmount) + " " + baseCurrency
    return (feePercentage/100)*baseCurrencyAmount

##
# Gets the current amount balance of a quote currency
# @param  {string}    quoteCurrency          the quote currency of the balance to be requested
# @return {float}    the amount balance of the currency requested
##
def getQuoteAmountBalance(quoteCurrency):
    #return str(currentBalance[quoteCurrency]) + " " + quoteCurrency
    return currentBalance[quoteCurrency]

##
# Returns a status of all balances
# @return {dict}    all current balances
##
def getAllQuotesBalance():
    return currentBalance

##
# Makes a transaction between two currencis
# @param  {string}   baseCurrency           the base currency of the rate
# @param  {string}   quoteCurrency          the quote currency of the rate
# @param  {float}    quoteCurrencyAmount    the amount the user wants to know the exchange of
# @return {float}    the exchange rate amount
##
def exchange(baseCurrency, quoteCurrency, quoteCurrencyAmount):
    price = getRate(quoteCurrency,baseCurrency,quoteCurrencyAmount)
    fee = getFeeCost(baseCurrency,price)
    totalTransactionCost = fee + price
    availableBalance = getQuoteAmountBalance(baseCurrency)
    #We check if there are sufficient funds on the currency we will charge a fee on
    if availableBalance >= totalTransactionCost:
        currentBalance[baseCurrency]  = currentBalance[baseCurrency] - totalTransactionCost
        currentBalance[quoteCurrency] = currentBalance[quoteCurrency] + quoteCurrencyAmount

        #we get the time of the transaction
        now = datetime.now()
        # dd/mm/YY H:M:S
        datetimeString = now.strftime("%d/%m/%Y %H:%M:%S")

        #we place the registry in the database. Our registries are sets of 3 values,
        #the base currency charged, the fee amount, and the time of the transaction
        feesDict["feeChargeRegistries"].append([baseCurrency, fee, datetimeString])

        feesRegistry = open("feesregistries.json", "w")
        json.dump(feesDict, feesRegistry)
        feesRegistry.close()
    else:
        raise Exception("Available balance amount of " + baseCurrency + " is insufficient." )

    return {"exchangeRate":price, "feeCost":fee, "quoteAmountBalance":currentBalance[quoteCurrency]}

##
# Calculates the total fees charged so far in USD from the transaction registries.
# @return {float}    the total fees charged so far in USD
##
def calculateTotalFees():
    amountInUSD = 0
    #we iterate all the fees charged registries
    for registry in feesDict["feeChargeRegistries"]:
        baseFee = registry[0]
        amount = registry[1]
        #we convert the charge to USD and add it to the sum
        amountInUSD = amountInUSD + getRate(baseFee,"USD",amount)

    return amountInUSD
