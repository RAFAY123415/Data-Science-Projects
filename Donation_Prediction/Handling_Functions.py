from Get_Objects import ReturnObjects


class HandlingFunctions:
    def __init__(self):
        self.Dataprep = ReturnObjects.Creating_Data_Prep_Object()
        self.Datapreprocess = ReturnObjects.Creating_Data_Preprocess_Object()
        self.Datamodelling = ReturnObjects.Creating_Data_Modelling_Object()
        self.Modelprediction=ReturnObjects.Creating_Model_Prediction_Object()

    def Model_Retraining(self, Teledata_Path, Call_logs_Path, Mapping_Path):

        Hashed_teledata, Hashed_call_logs_data, Mapping_data = self.Dataprep.Reading_Data(Teledata_Path, Call_logs_Path,Mapping_Path)
        Hashed_teledata = self.Dataprep.Convert_Format(Hashed_teledata)
        Hashed_teledata, Hashed_call_logs_data = self.Dataprep.DataDropping_Null_Values(Hashed_teledata,Hashed_call_logs_data)
        Donation_data = self.Dataprep.Combining_Data(Hashed_teledata, Hashed_call_logs_data, Mapping_data)
        Donation_data = self.Dataprep.Replacing_Values_Of_Target_Column(Donation_data)
        Donation_data = self.Dataprep.Drop_Duplicates(Donation_data)
        Donation_data = self.Dataprep.Standardize_Columns(Donation_data)
        Donation_data = self.Dataprep.Extract_Longitude_and_Latitude(Donation_data)
        Donation_data = self.Dataprep.Replacing_Again_Target_Column_Value(Donation_data)
        Donation_data = self.Dataprep.Feature_Extraction(Donation_data)
        Donation_data = self.Dataprep.Cleaning_Columns(Donation_data)
        Donation_data = self.Dataprep.Changing_Data_Type(Donation_data)
        Donation_data = self.Dataprep.Handling_Null_Value(Donation_data)
        Donation_data = self.Datapreprocess.Dropping_Columns(Donation_data)
        Donation_data = self.Datapreprocess.Categorical_Columns_Into_Numerical(Donation_data)
        X_train, X_test, y_train, y_test = self.Datapreprocess.Splitting_Data(Donation_data)
        X_train, y_train = self.Datapreprocess.Applying_Sampling_Technique(X_train, y_train)
        Trained_models = self.Datamodelling.Data_Modelling(X_train, y_train)
        Model_Name, best_Accuracy_Score_based_on_Precision, Precision_Score, Training_time, Model_Object = self.Datamodelling.Prediction_Score(X_test, y_test, Trained_models)

    def File_Prediction(self, Teledata_Path):
        Hashed_teledata = self.Dataprep.Reading_Prediction_File(Teledata_Path)
        Hashed_teledata = self.Dataprep.Convert_Format(Hashed_teledata)
        Hashed_teledata = self.Dataprep.Dropping_Null_Values(Hashed_teledata)
        Hashed_teledata=self.Dataprep.Standardize_Columns(Hashed_teledata)
        Hashed_teledata = self.Dataprep.Extract_Longitude_and_Latitude(Hashed_teledata)
        Hashed_teledata=self.Dataprep.Cleaning_Columns(self, Hashed_teledata)
        Hashed_teledata=self.Dataprep.Changing_Data_Type(Hashed_teledata)
        Hashed_teledata=self.Dataprep.Handling_Null_Value(Hashed_teledata)
        Donation_data = self.Datapreprocess.Dropping_Columns(Hashed_teledata)
        Donation_data=self.Datapreprocess.Changing_Target_Column_Value(Donation_data)
        Donation_data = self.Datapreprocess.Categorical_Variable_Mapping(Donation_data)
        Results=self.Modelprediction.Model_Prediction(Donation_data)






















