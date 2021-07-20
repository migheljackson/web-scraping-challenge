# import necessary libraries
import requests
import pymongo
from flask import Flask, render_template
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

    # Find one record of data from the mongo database
    #destination_data = mongo.db.collection.find_one()

    print('\n returned records:',len(mars_docs),'\n full record:',mars_docs)

    # Return template and data
    #return render_template("index.html", vacation=destination_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_scrape_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    db.mars_mission.update({}, mars_scrape_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True,port=5010)