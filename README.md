# README #


### Description ###

* This repository is an implementation for a currency exchange app challenge.
Apart from the use instructions to run your own API for this service, there's temporarily a container already running on an EC2 instance for you to use on http://52.27.34.128:7700/.
The service is built on python flask, with a local json file as our local database.
* Version 0.0

### Implementation ###

###### Docker Image
* Download
```shell
$ docker pull baronhotspur/currencyexchange
```
* Run the container. The service runs on port 7700. To use the localhost "0.0.0.0" instead of docker's default, we do a "-p" parameter.
```shell
$ docker container run -p 7700:7700 baronhotspur/currencyexchange
```
* The app will run automatically with the container and be ready to use.

### Use ###

###### POST getexchangerate
To get the exchange rate between a base currency and a quote currency, we specify both and the base currency amount to convert by sending the following data set:
    * API: [http://52.27.34.128:7700/getexchangerate](URL).
    * We send a POST request with the following information:
```    
    {
        "baseCurrency": "CAD",
        "baseCurrencyAmount": 1,
        "quoteCurrency": "GBP"
    }
```

The reply contains information about the exchange rate requested, in this example, we get 0.576 GBP for 1 CAD. We have set, for this project, a 3% fee on all transactions:
```
    {
        "exchangeRate": 0.576,
        "feeCost": 0.03,
        "quoteAmountBalance": 1000
    }
```
###### POST exchangecurrency
To exchange between two currencies, we provide the quoteCurrency amount to buy and the base currency to pay with:
    * API: [http://52.27.34.128:7700/exchangecurrency](URL).
    * We send a POST request with the following information:
```    
    {
        "baseCurrency": "CAD",
        "quoteCurrencyAmount": 1,
        "quoteCurrency": "GBP"
    }
```

The reply contains information about the exchange rate requested.:
```
    {
        "exchangeRate": 0.576,
        "feeCost": 0.03,
        "quoteAmountBalance": 1000
    }
```
###### GET calculatefees
A method to calculate the total fees charged amount so far in USD:
    * API: [http://52.27.34.128:7700/calculatefees](URL).
    * We get from the GET request the example following information:
```    
    {
        "USD": 0
    }
```

###### GET getallquotesbalance
A method to get the amount available for every currency:
    * API: [http://52.27.34.128:7700/getallquotesbalance](URL).
    * We get from the GET request the example following information:
```    
    {
        "USD": 1000,
        "GBP": 1000,
        "EUR": 1000,
        "JPY": 1000,
        "CHF": 1000,
        "AUD": 1000,
        "CAD": 1000,
        "NZD": 1000
    }
```



### Technical Specifications ###

##### currencyExchange_webhook.py
This file is the flask application.

##### currencyExchange.py
This file contains the business logic of the application.
1. **Getting the exchange rate** `getRate(baseCurrency, quoteCurrency, baseCurrencyAmount)`: The method simply applies division and multiplication to get the exchange rate according to the file's currency rates.
2. **Exchanging a currency**     `exchange(text)`: here we go through various steps to make a transaction between two currencies. First we calculate the total transaction amount by adding the fee charge to the amount conversion. Then we check if there are sufficient funds to make a transaction for that amount, else we raise a catchable exception. We register in the database `feesregistries.json` the time of the transaction, the currency and the fee charged, since we want to keep a record of that. We return as information the new balance amount for the currency bought, the fee for the currency it was bought with, and the exchange rate.
2. **Calculating total fees charged** `calculateTotalFees()`: here we iterate all the fee charges registered, convert them to USD and add them to the sum to report to the user.

##### test_currencyExchange.py
This file contains some unit tests for the application. For this occasion did not write tests for the API exposure methods, but only for the methods involving the business logic. I acknowledge the pertinence for writing methods for the API methods as well as much more and better unit tests for the core logic despite the time available.

##### feesregistries.json.
the file contains data structured in the following way:
```
{
  "feeChargeRegistries": [["CAD", 0.0, "14/07/2021 17:50:26"],["GBP", 1.0, "14/07/2021 17:52:26"]]
}
```
this is a registry of every fee charge done in list sets of 3.

### Contact the author ###

* Jose Eduardo Casillas (jose.e.casillas@gmail.com)
