from flask import Flask, request, make_response
from currencyExchange import *
import argparse
import os
import json

app = Flask(__name__)

##
# Confirms the service is working on a browser
# @return {dict} a symbolic confirmation of the service
##
@app.route("/", methods=["GET"])
def retornodummy():
    r = make_response("Currency Exchange Service Works")
    return r

##
# Provides the user with the exchange rate of two currencies
# @param  {dict}   contenido de la peticion a la funcion
        # {
        #     "baseCurrency":EUR,
        #     "baseCurrencyAmount":$$$,
        #     "quoteCurrency":GBP
        # }
# @return {dict}   a symbolic confirmation of the connection
        #{
        #      "exchangeRate":$$$
        #      "feeCost":$$$
        #      "quoteAmountBalance":$$$
        #}
##
@app.route("/getexchangerate", methods=["POST", "GET"])
def getexchangerate():
    req = request.get_json(silent=True, force=True)

    #we get the parameters we need from the request
    baseCurrency = req.get("baseCurrency")
    baseCurrencyAmount = req.get("baseCurrencyAmount")
    quoteCurrency = req.get("quoteCurrency")

    #we process the BUSINESS LOGIC to get the values requested by the user
    exchangeRate = getRate(baseCurrency, quoteCurrency,baseCurrencyAmount)
    feeCost = getFeeCost(baseCurrency,baseCurrencyAmount)
    quoteAmountBalance = getQuoteAmountBalance(quoteCurrency)

    res = {"exchangeRate":exchangeRate, "feeCost":feeCost, "quoteAmountBalance":quoteAmountBalance}

    # Construccion de respuesta en formato json
    # ********************************************
    res = json.dumps(res, indent=4)

    r = make_response(res)

    r.headers["Content-Type"] = "application/json"
    # ********************************************
    return r


##
# Makes a transaction between two currencies
# @param  {dict}   contenido de la peticion a la funcion
        # {
        #     "baseCurrency":EUR,
        #     "quoteCurrency":GBP
        #     "quoteCurrencyAmount": $$$
        # }
# @return {dict}   a symbolic confirmation of the connection
        #{
        #      "baseCurrencyBalance":$$$
        #      "quoteCurrencyBalance":$$$
        #}
##
@app.route("/exchangecurrency", methods=["POST"])
def exchangecurrency():
    req = request.get_json(silent=True, force=True)

    #we get the parameters we need from the request
    baseCurrency = req.get("baseCurrency")
    quoteCurrency = req.get("quoteCurrency")
    quoteCurrencyAmount = req.get("quoteCurrencyAmount")

    #we process the BUSINESS LOGIC to get the values requested by the user
    tradeDataSet = exchange(baseCurrency, quoteCurrency, quoteCurrencyAmount)


    res = {"exchangeRate":tradeDataSet["exchangeRate"], "feeCost":tradeDataSet["feeCost"], "quoteAmountBalance":tradeDataSet["quoteAmountBalance"]}

    # Construccion de respuesta en formato json
    # ********************************************
    res = json.dumps(res, indent=4)

    r = make_response(res)

    r.headers["Content-Type"] = "application/json"
    # ********************************************
    return r

##
# Provides the current balance statuses
# @return {dict}  the dict of the current balances
        #{"USD": 1000,
        #"GBP": 1000,
        #"EUR": 1000,
        #"JPY": 1000,
        # ...
        #}
##
@app.route("/getallquotesbalance", methods=["GET"])
def getallquotesbalance():
    res = getAllQuotesBalance()

    # Construccion de respuesta en formato json
    # ********************************************
    res = json.dumps(res, indent=4)

    r = make_response(res)

    r.headers["Content-Type"] = "application/json"
    # ********************************************
    return r

##
# Provides the user with the total amount of fees charged so far in USD
# @return {dict} a set with the amount charged
        #{"USD": 1000}
##
@app.route("/calculatefees", methods=["GET"])
def calculateFees():
    res = {"USD":calculateTotalFees()}

    # Construccion de respuesta en formato json
    # ********************************************
    res = json.dumps(res, indent=4)

    r = make_response(res)

    r.headers["Content-Type"] = "application/json"
    # ********************************************
    return r



##############################################################################################################################################
#MAIN PROCESS TO RUN THE FLASK SERVICE
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Currency Exchange Service')
    parser.add_argument('--port', dest='noport', metavar='NNNN', type=int, help='The port number for webservice listener')
    parser.add_argument('--debug', dest='debug', metavar='N', type=int, help='debug mode, 1 for turn on')
    args = parser.parse_args()
    # asignacion de puerto del webhook y modo debug
    # si el puerto no es asignado, se toma 7700 por default
    debug = bool(args.debug)
    # --------------------------------------------------------------------
    if args.noport is None:
        noport = 7700
    else:
        noport = args.noport

    port = int(os.getenv("PORT", noport))
    print("Starting app on port %d" %port)
    app.run(debug=debug, port=port, host="0.0.0.0")
