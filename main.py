import flask
from flask import Flask,jsonify, request, render_template
from twitter_tweet_Extraction import getTweets
from getSentiment import getSentiment
import pandas as pd
import json
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

stocksDB = {}

@app.route("/")
def index():
    return render_template('index.html')

# @app.route("/graph")
# def graph():
#     return render_template('base.html')


@app.route("/messages/<string:stock>", methods = ['GET'])
def get(stock):
    frame = pd.DataFrame()
    print(stocksDB.keys())
    if stock in stocksDB:
        print("Getting Data from Database")
        dataframe = pd.read_json(stocksDB.get(stock))
        jsonframe = stocksDB.get(stock)
    else:
        print("Getting new data : "+stock)
        dataframe = getSentiment(stock)
        jsonframe = dataframe.to_json()
        stocksDB[stock] = jsonframe
    # dataframe.plot(x='date', y=['text_blob','vader_sentiment'],kind = 'line',title = 'sentiment analysis for ' + stock, xlabel = 'Date', ylabel = 'sentiment')
    # plt.gca().legend(['Text Blob','Vader Sentiment'])
    # plt.show()
    dateC = json.dumps(dataframe['date'].dt.strftime('%Y-%m-%d').tolist())
    textblobC = json.dumps(dataframe['text_blob'].tolist())
    vaderC = json.dumps(dataframe['vader_sentiment'].tolist())
    realStock = json.dumps(dataframe['Adj Close'].tolist())
    # return jsonframe
    return render_template('base.html',date = dateC, tbC = textblobC, vC = vaderC,stock = stock,realStock = realStock)

if __name__ == "__main__":

    print("starting server...")
    
    with open('stockDB.json') as f:
        data = f.read()
    stocksDB = json.loads(data)
    # app.run(port = 81, debug=True)
    # app.run(debug=True, port=os.getenv("PORT", default=5000))
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT", default=5000))
    if stocksDB:
        a_file = open("stockDB.json", "w")
        json.dump(stocksDB, a_file)
        a_file.close()
    
    print("Bye....")
