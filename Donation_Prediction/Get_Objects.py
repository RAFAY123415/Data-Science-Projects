from Data_Preperation import DataPreperation
from Data_Preprocessing import DataProcessing
from Data_Modelling import DataModelling
from Model_Prediction import ModelPrediction


class ReturnObjects:
    @staticmethod
    def Creating_Data_Prep_Object():
        Dataprep = DataPreperation()
        return Dataprep

    @staticmethod
    def Creating_Data_Preprocess_Object():
        Datapreprocess = DataProcessing()
        return Datapreprocess

    @staticmethod
    def Creating_Data_Modelling_Object():
        Datamodelling = DataModelling()
        return Datamodelling

    @staticmethod
    def Creating_Model_Prediction_Object():
        modelprediction = ModelPrediction()
        return modelprediction
