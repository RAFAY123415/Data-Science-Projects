from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from flask import Flask, request, jsonify
import joblib
import pickle
import numpy as np
from geopy.distance import geodesic


app = Flask(__name__)
CORS(app)

model = joblib.load("best_regressor_model.pkl")
input_scaler = joblib.load("input_scaler.pkl")
output_scaler = joblib.load("output_scaler.pkl")

@app.route('/price', methods=['POST'])
def predict_price():
    data = request.json
  # Convert JSON to DataFrame
    dataframe = pd.DataFrame([data])

    neighborhood_coords = {'Roxbury': {'latitude': 42.32642574, 'longitude': -71.09581055}, 'Beacon Hill': {'latitude': 42.3603, 'longitude': -71.06588}, 'Dorchester': {'latitude': 42.31656979, 'longitude': -71.05215552}, 'Charlestown': {'latitude': 42.37321342, 'longitude': -71.06162061}, 'Jamaica Plain': {'latitude': 42.31672295, 'longitude': -71.11642095}, 'North End': {'latitude': 42.34399646, 'longitude': -71.06372085}, 'South Boston': {'latitude': 42.33483, 'longitude': -71.03652}, 'Back Bay': {'latitude': 42.33511, 'longitude': -71.07756}, 'Roslindale': {'latitude': 42.28117408, 'longitude': -71.1538144}, 'Downtown Crossing': {'latitude': 42.3544, 'longitude': -71.06039}, 'South End': {'latitude': 42.34583822, 'longitude': -71.06497243}, 'Government Center': {'latitude': 42.3597641, 'longitude': -71.06116486}, 'West End': {'latitude': 42.36548, 'longitude': -71.06833}, 'Allston-Brighton': {'latitude': 42.3496, 'longitude': -71.07185}, 'Fenway/Kenmore': {'latitude': 42.34742, 'longitude': -71.10491}, 'Hyde Park': {'latitude': 42.25150597, 'longitude': -71.13251906}, 'West Roxbury': {'latitude': 42.27816883, 'longitude': -71.14712801}, 'East Boston': {'latitude': 42.38606, 'longitude': -71.00721}, 'Mattapan': {'latitude': 42.27348827, 'longitude': -71.09552801}, 'Leather District': {'latitude': 42.36681, 'longitude': -71.05615}, 'Mission Hill': {'latitude': 42.32644622, 'longitude': -71.10001127}, 'Chinatown': {'latitude': 42.34873, 'longitude': -71.06069}, 'Theater District': {'latitude': 42.35112845, 'longitude': -71.06420764}, 'Cape Neddick': {'latitude': 42.3488792, 'longitude': -71.0688545}, 'Cambridge': {'latitude': 42.38356, 'longitude': -71.07874}, 'Downtown': {'latitude': 42.36239317, 'longitude': -71.05249589}, 'Chestnut Hill': {'latitude': 42.301319, 'longitude': -71.165781}, 'Back Bay West': {'latitude': 42.34988, 'longitude': -71.08989}, 'Brighton': {'latitude': 42.34949865, 'longitude': -71.17344584}, 'Harwich Port': {'latitude': 42.37327, 'longitude': -71.05859}, 'Spring Hill': {'latitude': 42.36474704, 'longitude': -71.05588948}, 'Brookline': {'latitude': 42.34832941, 'longitude': -71.07179036}, 'East Downtown': {'latitude': 42.34575, 'longitude': -71.07357}, 'Lower Allston': {'latitude': 42.36193717, 'longitude': -71.13295433}, 'Prudential / St. Botolph': {'latitude': 42.34395939, 'longitude': -71.08339092}, 'D Street / West Broadway': {'latitude': 42.34797971, 'longitude': -71.10197428}, 'Bay Village': {'latitude': 42.34982, 'longitude': -71.06879}, 'Boston Theater District': {'latitude': 42.36032, 'longitude': -71.1432}, 'Eagle Hill': {'latitude': 42.37678842, 'longitude': -71.03961242}, 'Jeffries Point': {'latitude': 42.36743, 'longitude': -71.03544}, 'Fenway–Kenmore': {'latitude': 42.34772055, 'longitude': -71.09336078}, 'Allston': {'latitude': 42.36124351, 'longitude': -71.124509}, 'Stony Brook / Cleary Square': {'latitude': 42.25809, 'longitude': -71.12244}, 'Columbus Park / Andrew Square': {'latitude': 42.3325797, 'longitude': -71.0484071}, 'Codman Square': {'latitude': 42.30824, 'longitude': -71.08452}, 'Central City': {'latitude': 42.31493672, 'longitude': -71.05546264}, "St. Elizabeth's": {'latitude': 42.33999007, 'longitude': -71.1553969}, 'Harvard Square': {'latitude': 42.36033286, 'longitude': -71.0709537}, 'Franklin Field South': {'latitude': 42.28967849, 'longitude': -71.0800464}, 'Brewster': {'latitude': 42.339042, 'longitude': -71.0803574}, 'City Point': {'latitude': 42.33581, 'longitude': -71.03809}, 'Cedar Grove': {'latitude': 42.28487357, 'longitude': -71.04756586}, 'West Fens': {'latitude': 42.34097, 'longitude': -71.09694}, 'Fisher Hill': {'latitude': 42.33855, 'longitude': -71.14882}, 'Rockport': {'latitude': 42.37449, 'longitude': -71.06198}, 'East Falmouth': {'latitude': 42.28288, 'longitude': -71.139}, 'Orient Heights': {'latitude': 42.38831, 'longitude': -70.996}, 'Franklin Field North': {'latitude': 42.2959361, 'longitude': -71.0808318}, 'Ward Two': {'latitude': 42.36845, 'longitude': -71.03757}, 'Southern Mattapan': {'latitude': 42.26976, 'longitude': -71.08894}, 'Metropolitan Hill / Beech Street': {'latitude': 42.28509, 'longitude': -71.14088}, 'Harbor View / Orient Heights': {'latitude': 42.37688, 'longitude': -71.02791}, 'Sun Bay South': {'latitude': 42.34670877, 'longitude': -71.15158383}, 'Newton': {'latitude': 42.35040321, 'longitude': -71.06369056}, 'Wellington Hill': {'latitude': 42.28326, 'longitude': -71.09263}, 'Brook Farm': {'latitude': 42.29362, 'longitude': -71.13868}, 'South Sanford': {'latitude': 42.3359355, 'longitude': -71.04609542}, 'Dorchester Center': {'latitude': 42.27987, 'longitude': -71.05947}, 'Commonwealth': {'latitude': 42.3385253, 'longitude': -71.1508895}, 'Medford Street / The Neck': {'latitude': 42.38045, 'longitude': -71.07001}, 'West Street / River Street': {'latitude': 42.27131552, 'longitude': -71.12159059}, 'Lower Washington / Mount Hope': {'latitude': 42.2821, 'longitude': -71.12259}, 'South Medford': {'latitude': 42.28938, 'longitude': -71.04194}, 'Vineyard Haven': {'latitude': 42.35846, 'longitude': -71.07213}, 'Fairmount Hill': {'latitude': 42.24472839, 'longitude': -71.12051106}, 'South Beach': {'latitude': 42.36539578, 'longitude': -71.05525976}, 'Uplands': {'latitude': 42.32563, 'longitude': -71.07994}}
    dataframe['Latitude'] = dataframe['Host_neighbourhood'].map(lambda x: neighborhood_coords.get(x, {}).get('latitude'))
    dataframe['Longitude'] = dataframe['Host_neighbourhood'].map(lambda x: neighborhood_coords.get(x, {}).get('longitude'))

    city_center_coords = (42.3601, -71.0589)  # These are Bosten City Center Coordinates.
    dataframe['Distance_from_city_center_km'] = dataframe.apply(lambda row: geodesic((row['Latitude'], row['Longitude']), city_center_coords).km, axis=1)
    dataframe =dataframe[['Host_response_time', 'Host_response_rate', 'Host_acceptance_rate', 'Host_is_superhost', 'Host_neighbourhood', 'Host_identity_verified', 'Latitude', 'Longitude', 'Property_type', 'Room_type', 'Accommodates', 'Bathrooms', 'Bedrooms', 'Beds', 'Minimum_nights', 'Maximum_nights', 'Number_of_reviews_ltm', 'Number_of_reviews_l30d', 'Review_scores_rating', 'Review_scores_accuracy', 'Review_scores_cleanliness', 'Review_scores_checkin', 'Review_scores_communication', 'Review_scores_location', 'Review_scores_value', 'Instant_bookable', 'Distance_from_city_center_km', 'Having_License']]
    numerical_cols = dataframe.select_dtypes(include=['float64', 'int64']).columns
    X_scaled = input_scaler.transform(dataframe[numerical_cols])
    dataframe[numerical_cols] = X_scaled
    bool_cols = dataframe.select_dtypes(include=['bool']).columns
    dataframe[bool_cols] = dataframe[bool_cols].astype(int)
    dataframe['Room_type'].replace({'Entire home/apt': 0, 'Private room': 1, 'Shared room': 2, 'Hotel room': 3}, inplace=True)
    dataframe['Property_type'].replace({'Entire guest suite': 0, 'Entire condo': 1, 'Entire rental unit': 2, 'Private room in home': 3, 'Private room in rental unit': 4, 'Private room in townhouse': 5, 'Private room in condo': 6, 'Entire home': 7, 'Entire townhouse': 8, 'Entire loft': 9, 'Private room in bed and breakfast': 10, 'Shared room in home': 11, 'Entire guesthouse': 12, 'Entire serviced apartment': 13, 'Private room in guest suite': 14, 'Private room': 15, 'Private room in bungalow': 16, 'Private room in loft': 17, 'Entire place': 18, 'Private room in guesthouse': 19, 'Room in boutique hotel': 20, 'Shared room in townhouse': 21, 'Private room in serviced apartment': 22, 'Shared room in boutique hotel': 23, 'Private room in casa particular': 24, 'Boat': 25, 'Shared room in condo': 26, 'Private room in vacation home': 27, 'Shared room in vacation home': 28, 'Room in aparthotel': 29, 'Entire vacation home': 30, 'Shared room in rental unit': 31, 'Private room in villa': 32}, inplace=True)
    dataframe['Host_neighbourhood'].replace({'Roxbury': 0, 'Beacon Hill': 1, 'Dorchester': 2, 'Charlestown': 3, 'Jamaica Plain': 4, 'North End': 5, 'South Boston': 6, 'Back Bay': 7, 'Roslindale': 8, 'Downtown Crossing': 9, 'South End': 10, 'Government Center': 11, 'West End': 12, np.nan: -1, 'Allston-Brighton': 13, 'Fenway/Kenmore': 14, 'Hyde Park': 15, 'West Roxbury': 16, 'East Boston': 17, 'Mattapan': 18, 'Leather District': 19, 'Mission Hill': 20, 'Chinatown': 21, 'Theater District': 22, 'Cape Neddick': 23, 'Cambridge': 24, 'Downtown': 25, 'Chestnut Hill': 26, 'Back Bay West': 27, 'Brighton': 28, 'Harwich Port': 29, 'Spring Hill': 30, 'Brookline': 31, 'East Downtown': 32, 'Lower Allston': 33, 'Prudential / St. Botolph': 34, 'D Street / West Broadway': 35, 'Bay Village': 36, 'Boston Theater District': 37, 'Eagle Hill': 38, 'Jeffries Point': 39, 'Fenway–Kenmore': 40, 'Allston': 41, 'Stony Brook / Cleary Square': 42, 'Columbus Park / Andrew Square': 43, 'Codman Square': 44, 'Central City': 45, "St. Elizabeth's": 46, 'Harvard Square': 47, 'Franklin Field South': 48, 'Brewster': 49, 'City Point': 50, 'Cedar Grove': 51, 'West Fens': 52, 'Fisher Hill': 53, 'Rockport': 54, 'East Falmouth': 55, 'Orient Heights': 56, 'Franklin Field North': 57, 'Ward Two': 58, 'Southern Mattapan': 59, 'Metropolitan Hill / Beech Street': 60, 'Harbor View / Orient Heights': 61, 'Sun Bay South': 62, 'Newton': 63, 'Wellington Hill': 64, 'Brook Farm': 65, 'South Sanford': 66, 'Dorchester Center': 67, 'Commonwealth': 68, 'Medford Street / The Neck': 69, 'West Street / River Street': 70, 'Lower Washington / Mount Hope': 71, 'South Medford': 72, 'Vineyard Haven': 73, 'Fairmount Hill': 74, 'South Beach': 75, 'Uplands': 76}, inplace=True)
    dataframe['Host_response_time'].replace({'Fast': 0, 'Moderate': 1, 'Slow': 2}, inplace=True)

    dataframe = dataframe.round({col: 2 for col in dataframe.select_dtypes(include='float').columns})
    # Make predictions
    scaled_prediction = model.predict(dataframe)

    # If target (output) was scaled, inverse the transformation to get the original scale
    prediction = output_scaler.inverse_transform(scaled_prediction.reshape(-1, 1))
    predicted_price = round(prediction[0][0], 2)

    response_data = {
        "price":  predicted_price,
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
