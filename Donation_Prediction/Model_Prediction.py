import pickle


class ModelPrediction:
    def __init__(self):
        self.Machine_Learning_Model = pickle.load(open('KNN.sav', 'rb'))

    def Model_Prediction(self, X_test):
        X_test = X_test.to_numpy()
        y_predict = self.Machine_Learning_Model.predict(X_test)
        return y_predict
