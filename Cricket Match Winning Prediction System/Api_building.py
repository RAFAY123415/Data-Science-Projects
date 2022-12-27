'''
The purpose of this class is to build api that would take the input csv and stored it and return the
path of csv with prediction.
'''
# importing Library
import pickle
import pandas as pd 

class Api_Building :
    def __init__(self) :
        self.filename = 'Random_Forest_Model.sav'
        self.random_forest = pickle.load(open(self.filename, 'rb'))

    def Api_Development(self,path) :
        df=pd.read_csv(path)
        prediction_input=df.loc[(df['balls_left']<60)&(df['target']>120)]
        prediction_values=self.random_forest.predict(prediction_input)
        prediction_input['Prediction_Results']=prediction_values.tolist()
        prediction_input.to_csv('result.csv',index=False)
        return 'result.csv'






    

