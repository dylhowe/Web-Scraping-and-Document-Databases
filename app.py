# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsdata"
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data

    marsdata = mongo.db.marsdata.find_one()


    # return template and data
    return render_template("index.html", marsdata = marsdata)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    mars_return = scrape_mars.scrape()

    # Store results into a dictionary
    mars_return_dict = {
        "article_title": mars_return["article_title"],
        "article_teaser": mars_return["article_teaser"],
        "big_img_url": mars_return["big_img_url"],
        "mars_weather": mars_return["mars_weather"],
        "facts_html": mars_return["facts_html"],
        "titles_urls": mars_return["titles_urls"],
    }

    # Insert mars return into database
    mongo.db.drop_collection("marsdata")
    mongo.db.marsdata.insert_one(mars_return_dict)

        # Redirect back to home page
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)
