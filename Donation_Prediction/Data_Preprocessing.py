import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
import json

plt.rcParams.update({'figure.figsize': (7, 5), 'figure.dpi': 100})


class DataProcessing:
    '''def Reading_File(self,Donation_data):
        donation_data = pd.read_csv(Donation_data + "/*.csv", encoding='latin-1', low_memory=False)

        return donation_data'''

    def Dropping_Columns_List(self):
        return ['baseid', 'fornavn', 'efternavn', 'adresse', 'vej', 'husnr', 'bogstav', 'sal', 'side', 'kvhx',
                'telephone', 'hashed_telephone', 'postnummer', 'kommunekode',
                'call_ending_reason', 'tlfnr', 'udd_erhvervsgymasial',
                'stednavn', 'bynavn', 'tlftype1', 'tlftype2', 'tlftype3',
                'tlftype4', 'tlftype5', 'meaning', 'call_date', 'call_time', 'date_and_time', 'weekday_or_weekend',
                'day', 'month', 'year', 'hour', 'minute', 'week_of_year']

    def Dropping_Columns(self, Donation_data):
        list_of_dropping_columns = self.Dropping_Columns_List()
        for col in list_of_dropping_columns:
            try:
                Donation_data.drop(col, axis=1, inplace=True)
            except:
                continue

        return Donation_data

    def Changing_Target_Column_Value(self, Donation_data):
        Donation_data['target_column'].replace({'Yes': 1, 'No': 0, 'Unfinished': -1}, inplace=True)
        return Donation_data

    def Categorical_Variable_Mapping(self, Donation_data):
        json_file = open('sample.json')
        column_values = json.load(json_file)
        for key, values in column_values.items():
            Donation_data[key].replace(values, inplace=True)

        json_file.close()

        return Donation_data

    '''
    def Categorical_Columns_Into_Numerical(self,Donation_data):
        for col in ['koen', 'mosaic_gruppe', 'mosaic_type', 'okonomisk_formaaen', 'ejerforhold', 'enhedsanvendelse']:
            mapping_data = Donation_data[col].value_counts().reset_index()
            mapping_data.drop([col], axis=1, inplace=True)
            mapping_data = mapping_data.to_dict()
            mapping_data = mapping_data['index']
            mapping_data = {y: x for x, y in mapping_data.items()}
            Donation_data[col].replace(mapping_data, inplace=True)

        return Donation_data
        
    '''

    def Splitting_Data(self, Donation_data):
        Y = Donation_data['target_column']
        X = Donation_data.drop(['target_column'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0, stratify=Y)

        return X_train, X_test, y_train, y_test

    def Applying_Sampling_Technique(self, X_train, y_train):
        oversample = SMOTE(sampling_strategy='minority')
        X_train, y_train = oversample.fit_resample(X_train, y_train)

        return X_train, y_train
