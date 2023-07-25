from flask import Flask, render_template, url_for, request 
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup as bs
import requests
import pymongo


app = Flask(__name__)


@app.route("/")
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/review", methods=["POST", "GET"])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            search_string = request.form["content"].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string
            flipkart_req = requests.get(flipkart_url)
            flipkart_html = bs( flipkart_req.text, "html.parser" )
            bigboxes = flipkart_html.find_all("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a["href"]
            prod_req = requests.get( productLink )
            prod_req.encoding = "utf-8"
            prod_html = bs( prod_req.text, "html.parser" )
            commentBoxes = prod_html.find_all("div", {"class": "_16PBlm"})

            reviews = []
            for commentBox in commentBoxes:
                try:
                    name = commentBox.find_all("p", {"class": "_2sc7ZR _2V5EHH"})[0].text
                except:
                    name = "no name"

                try:
                    rating = commentBox.div.div.div.div.text
                except:
                    rating = "No rating"

                try:
                    commentHead = commentBox.div.div.div.p.text
                except:
                    commentHead = "No comment head"

                try:
                    commentTag = commentBox.find_all("div", {"class":""})[0].div.text
                except:
                    commentTag = "No comment Tag"

                mydict = {"Product" : search_string, "Name" : name , "Rating" : rating, "CommentHead" : commentHead, "Comment" : commentTag}
                reviews.append(mydict)

            return render_template("results.html" , reviews =reviews[0:(len(reviews)-1)] )
        

        except Exception as e:
            return "Something is wrong : " + str(e)  
    
    else:
        return render_template("index.html")


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)