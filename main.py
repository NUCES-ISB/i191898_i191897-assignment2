from sklearn.linear_model import LogisticRegression
import pickle
from flask import Flask, request, jsonify,render_template
import requests
import json
import random

# # Load the dataset
# data = pd.read_csv("swarming_dataset.csv")

# # Split the data into features and labels
# X = data.drop("Swarming", axis=1)
# y = data["Swarming"]

# # Train a logistic regression model
# model = LogisticRegression()
# model.fit(X, y)

# # Save the model to a pickle file
# with open("model.pkl", "wb") as f:
#     pickle.dump(model, f)

# Create a Flask application
app = Flask(__name__)


temps = []
humids = []
sounds = []
preds = []
# Define a route for the live dashboard mod


@app.route("/")
def dashboard():
    # Load live data and predict swarming using the trained model
    # Display different metrics of the model on the dashboard
    host = "159.203.147.149:8080"
    #host = "localhost:8080"

    # set the API endpoint
    endpoint = "/api/data"

    # send a GET request to the endpoint
    response = requests.get(f"http://{host}{endpoint}", stream=True)

    count=0
    # iterate over the response stream
    for line in response.iter_lines():
        if line:
            try:
                # process the received data
                d=line.decode('utf-8').split('data:')[1]
                data=json.loads(d)
                instance=[data['Temperature'],data['Humidity'],data['Sound']]


                temp = data['Temperature']
                humid = data['Humidity']
                sound = data['Sound']

                # add live data to the respective lists
                temps.append(temp)
                humids.append(humid)
                sounds.append(sound)
                # Load the trained model from the pickle file
                with open("model.pkl", "rb") as f:
                    model = pickle.load(f)

                prediction = model.predict([instance])[0]
                preds.append(prediction)
                count+=1
            except:
                continue
            if count==10:
                break

    data=zip(temps, humids,sounds,preds)
    return render_template('dashboard.html', data=zip(temps,humids,sounds,preds))

# Define a route for the service mode
@app.route("/service", methods=["POST"])
def service():
    # Get an instance of live data from the user
    instance = request.json['data']

    # Load the trained model from the pickle file
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    # Predict swarming for the instance of live data using the trained model
    prediction = model.predict([instance])

    # Return the prediction to the user as JSON
    return jsonify({"prediction": prediction.tolist()})

if __name__ == "__main__":
    app.run(debug=True)
