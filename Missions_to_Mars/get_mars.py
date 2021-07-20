# import necessary libraries
import requests
import pymongo
from flask import Flask, render_template, redirect
import scrape_mars

#Create a Flask instance
app = Flask(__name__)

#GET all data from mongodb
conn = 'mongodb+srv://admin:admin@cluster0.5lstl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = pymongo.MongoClient(conn)
db = client.dr_claw
collection = db.mars_mission
mars_docs = db.mars_mission.find_one()

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    #Debug
    print("Server received request for 'Home' page...")
    print('\n returned records:\n',mars_docs)

    # Return template and data
    return render_template("index.html", mars_docs=mars_docs)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_scrape_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    db.mars_mission.replace_one({}, mars_scrape_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True,port=5010)