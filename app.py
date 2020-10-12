from flask import Flask

# Create an app, being sure to pass __name__
app = Flask(__name__)

# define what to do when a user hits the index route
@app.route("/")
def home():
    # Add back end print statements
    print("Server received request for 'Home' page...")
    # print out all available routes
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

if __name__ == '__main__':
    app.run(debug=True)