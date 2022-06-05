# Importing libraries
import numpy as np
import pandas as pd
import pgeocode
import ssl


class DataPreperation:

    def Column_Standards(self):
        Teledata_column_list = ['baseid', 'fornavn', 'efternavn', 'adresse', 'stednavn', 'postnummer',
                                'bynavn', 'kommunekode', 'vej', 'husnr', 'bogstav', 'sal', 'side',
                                'kvhx', 'robinson', 'tlftype1', 'tlftype2', 'tlftype3', 'tlftype4', 'tlftype5', 'koen',
                                'alder', 'mosaic_gruppe', 'mosaic_type', 'ssh_0_born', 'ssh_1_barn',
                                'ssh_2_born', 'ssh_3_plus_born', 'udd_grundskole',
                                'udd_almen_gymnasial', 'udd_erhvervsgymasial',
                                'udd_erhvervsfaglig_forloeb', 'udd_kort_videregaaende',
                                'udd_mellemlang_videregaaende', 'udd_bachelor',
                                'udd_lang_videregaaende', 'udd_forsker', 'udd_uoplyst',
                                'socio_high_selvst', 'socio_mellemniveau', 'socio_grundniveau',
                                'socio_ledig_kontant', 'socio_pensionist', 'socio_other',
                                'civilstand_ugift', 'civilstand_gift', 'civilstand_skilt',
                                'civilstand_enke', 'okonomisk_formaaen', 'antal_beboere',
                                'husstandsindkomst', 'ssh_anden_hustype', 'ssh_enlig_m_born',
                                'ssh_enlig_u_born', 'ssh_par_m_born', 'ssh_par_u_born', 'donation_ssh',
                                'donation_gns', 'ejerforhold', 'enhedsanvendelse', 'antal_vaerelser']
        Call_logs_columns_list = ['tlfnr', 'reason', 'call_date']
        Mapping_columns = ['call_ending_reason', 'meaning', 'Yes/no/unfinished']
        return Teledata_column_list, Call_logs_columns_list, Mapping_columns

    def Reading_Prediction_File(self, Teledata):
        Teledata_columns, Call_logs_columns, Mapping_columns = self.Column_Standards()
        Hashed_teledata = pd.read_csv(Teledata, encoding='latin-1', low_memory=False)
        for cols in Hashed_teledata.columns:
            if cols not in Teledata_columns:
                raise ValueError('Column Name :', cols, 'Not Found in Standard Columns of ', Teledata)

        return Hashed_teledata

    def Reading_Data(self, Teledata, Call_logs, Mapping):
        Teledata_columns, Call_logs_columns, Mapping_columns = self.Column_Standards()
        Hashed_teledata = pd.read_csv(Teledata, encoding='latin-1', low_memory=False)
        Hashed_call_logs = pd.read_csv(Call_logs, encoding='latin-1', low_memory=False)
        Mapping_data = pd.read_csv(Mapping, encoding='latin-1', low_memory=False)
        for cols in Hashed_teledata.columns:
            if cols not in Teledata_columns:
                raise ValueError('Column Name :', cols, 'Not Found in Standard Columns of ', Teledata)
        for cols in Hashed_call_logs.columns:
            if cols not in Call_logs_columns:
                raise ValueError('Column Name :', cols, 'Not Found in Standard Columns of ', Call_logs)
        for cols in Mapping_data.columns:
            if cols not in Mapping_columns:
                raise ValueError('Column Name :', cols, 'Not Found in Standard Columns of ', Mapping)

        return Hashed_teledata, Hashed_call_logs, Mapping_data

    def Convert_Format(self, Teledata):
        Teledata = Teledata.melt(id_vars=['baseid', 'fornavn', 'efternavn', 'adresse', 'stednavn', 'postnummer',
                                          'bynavn', 'kommunekode', 'vej', 'husnr', 'bogstav', 'sal', 'side',
                                          'kvhx', 'robinson', 'tlftype1', 'tlftype2', 'tlftype3', 'tlftype4',
                                          'tlftype5', 'koen',
                                          'alder', 'mosaic_gruppe', 'mosaic_type', 'ssh_0_born', 'ssh_1_barn',
                                          'ssh_2_born', 'ssh_3_plus_born', 'udd_grundskole',
                                          'udd_almen_gymnasial', 'udd_erhvervsgymasial',
                                          'udd_erhvervsfaglig_forloeb', 'udd_kort_videregaaende',
                                          'udd_mellemlang_videregaaende', 'udd_bachelor',
                                          'udd_lang_videregaaende', 'udd_forsker', 'udd_uoplyst',
                                          'socio_high_selvst', 'socio_mellemniveau', 'socio_grundniveau',
                                          'socio_ledig_kontant', 'socio_pensionist', 'socio_other',
                                          'civilstand_ugift', 'civilstand_gift', 'civilstand_skilt',
                                          'civilstand_enke', 'okonomisk_formaaen', 'antal_beboere',
                                          'husstandsindkomst', 'ssh_anden_hustype', 'ssh_enlig_m_born',
                                          'ssh_enlig_u_born', 'ssh_par_m_born', 'ssh_par_u_born', 'donation_ssh',
                                          'donation_gns', 'ejerforhold', 'enhedsanvendelse', 'antal_vaerelser'],
                                 var_name="telephone",
                                 value_name="hashed_telephone")

        return Teledata

    def Dropping_Null_Values(self, Teledata, Call_logs=None):
        if Teledata is not None and Call_logs is None:
            Teledata.dropna(subset=['hashed_telephone'], inplace=True)
            return Teledata
        if Teledata is None and Call_logs is not None :
            Call_logs.dropna(subset=['tlfnr'], inplace=True)
            return Call_logs
        else :
            return Teledata,Call_logs

    def Combining_Data(self, Teledata, Call_logs, Mapping):
        combine_data_file_1 = pd.merge(Teledata, Call_logs, how='inner', left_on=['hashed_telephone'],
                                       right_on=['tlfnr'])
        donation_data_file_1 = pd.merge(combine_data_file_1, Mapping, how='inner', left_on=['reason'],
                                        right_on=['call_ending_reason'])

        return donation_data_file_1

    def Replacing_Values_Of_Target_Column(self, Donation_data):
        return Donation_data['Yes/no/unfinished'].replace({'Yes': 1, 'No': 2, 'Unfinished': 3}, inplace=True)

    def Drop_Duplicates(self, Donation_data):
        Donation_data.drop_duplicates(subset=['call_ending_reason', 'Yes/no/unfinished', 'baseid'], inplace=True)
        Donation_data.sort_values(by=['Yes/no/unfinished'], inplace=True)
        Donation_data.drop_duplicates(subset=['baseid'], inplace=True, keep='first')

        return Donation_data

    def Standardize_Columns(self, Donation_data):
        return Donation_data.rename(columns={"Yes/no/unfinished": "target_column"}, inplace=True)

    def convert_post_to_lat(self, post_number):
        nomi = pgeocode.Nominatim('dk')
        data_frame = nomi.query_postal_code(str(post_number))

        return data_frame['latitude']

    def convert_post_to_long(self, post_number):
        nomi = pgeocode.Nominatim('dk')
        data_frame = nomi.query_postal_code(str(post_number))

        return data_frame['longitude']

    def Extract_Longitude_and_Latitude(self, Donation_data):
        nomi = pgeocode.Nominatim('dk')
        ssl._create_default_https_context = ssl._create_unverified_context
        post_numbers = Donation_data['postnummer'].tolist()
        post_numbers = map(str, post_numbers)
        query = nomi.query_postal_code(post_numbers)
        Donation_data['latitude'] = query['latitude']
        Donation_data['longitude'] = query['longitude']

        return Donation_data

    def Replacing_Again_Target_Column_Value(self, Donation_data):
        return Donation_data["target_column"].replace({2: 0, 3: -1}, inplace=True)

    def Feature_Extraction(self, Donation_data):
        Donation_data['Call_date'] = pd.to_datetime(Donation_data['call_date']).dt.strftime("%d-%m-%Y")
        Donation_data['Call_time'] = pd.to_datetime(Donation_data['call_date']).dt.strftime("%H:%M")
        Donation_data['date_and_time'] = pd.to_datetime(Donation_data['Call_date'] + ' ' + Donation_data['Call_time'])
        # day
        Donation_data['day'] = Donation_data['date_and_time'].dt.day
        # month
        Donation_data['month'] = Donation_data['date_and_time'].dt.month
        # year
        Donation_data['year'] = Donation_data['date_and_time'].dt.year
        # hour
        Donation_data['hour'] = Donation_data['date_and_time'].dt.hour
        # minute
        Donation_data['minute'] = Donation_data['date_and_time'].dt.minute
        # Monday is 0 and Sunday is 6
        Donation_data['weekday_or_weekend'] = Donation_data['date_and_time'].dt.weekday
        # week of the year
        Donation_data['week_of_year'] = Donation_data['date_and_time'].dt.isocalendar().week

        Donation_data['weekday_or_weekend'] = Donation_data['weekday_or_weekend'].replace(
            {0: "WeekDay", 1: "WeekDay", 2: "WeekDay", 3: "WeekDay", 4: "WeekDay",
             5: "Weekend", 6: "Weekend"})

        return Donation_data

    def Cleaning_Columns(self, Donation_data):

        for col in ['ssh_0_born', 'ssh_1_barn', 'ssh_2_born', 'ssh_3_plus_born', 'udd_grundskole',
                    'udd_almen_gymnasial',
                    'udd_erhvervsfaglig_forloeb', 'udd_kort_videregaaende', 'udd_mellemlang_videregaaende',
                    'udd_bachelor',
                    'udd_lang_videregaaende', 'udd_forsker', 'udd_uoplyst', 'socio_high_selvst', 'socio_mellemniveau',
                    'socio_grundniveau', 'socio_ledig_kontant', 'socio_pensionist', 'socio_other', 'civilstand_ugift',
                    'civilstand_gift', 'civilstand_skilt', 'civilstand_enke', 'antal_beboere', 'husstandsindkomst',
                    'ssh_anden_hustype', 'ssh_enlig_m_born', 'ssh_enlig_u_born', 'ssh_par_m_born', 'ssh_par_u_born',
                    'donation_ssh', 'donation_gns', 'antal_vaerelser']:
            try:
                Donation_data[col] = Donation_data[col].str.replace(',', '.')
            except:
                continue

        return Donation_data

    def Changing_Data_Type(self, Donation_data):
        for col in ['ssh_0_born', 'ssh_1_barn', 'ssh_2_born', 'ssh_3_plus_born', 'udd_grundskole',
                    'udd_almen_gymnasial',
                    'udd_erhvervsfaglig_forloeb', 'udd_kort_videregaaende', 'udd_mellemlang_videregaaende',
                    'udd_bachelor',
                    'udd_lang_videregaaende', 'udd_forsker', 'udd_uoplyst', 'socio_high_selvst', 'socio_mellemniveau',
                    'socio_grundniveau', 'socio_ledig_kontant', 'socio_pensionist', 'socio_other', 'civilstand_ugift',
                    'civilstand_gift', 'civilstand_skilt', 'civilstand_enke', 'ssh_anden_hustype', 'ssh_enlig_m_born',
                    'ssh_enlig_u_born', 'ssh_par_m_born', 'ssh_par_u_born']:
            try:
                Donation_data[col] = pd.to_numeric(Donation_data[col], downcast="float")
                Donation_data[col] = Donation_data[col].round(2)
            except:
                continue

        for col in ['antal_vaerelser', 'donation_gns', 'donation_ssh', 'antal_beboere', 'husstandsindkomst']:
            try:
                Donation_data[col] = Donation_data[col].replace({np.nan: -1})
                Donation_data[col] = Donation_data[col].astype('int')
            except:
                continue

        return Donation_data

    def Handling_Null_Value(self, Donation_data):
        for cols in ['koen', 'mosaic_gruppe', 'mosaic_type', 'okonomisk_formaaen', 'ejerforhold',
                     'enhedsanvendelse', 'call_date', 'call_time', 'date_and_time', 'weekday_or_weekend']:
            try:
                if Donation_data[cols].isna().sum() > 0:
                    Donation_data[cols].replace({np.nan: 'Other'}, inplace=True)
            except:
                continue

        for cols in ['alder', 'ssh_0_born', 'ssh_1_barn', 'ssh_2_born', 'ssh_3_plus_born', 'udd_grundskole',
                     'udd_almen_gymnasial', 'udd_erhvervsgymasial', 'udd_erhvervsfaglig_forloeb',
                     'udd_kort_videregaaende', 'udd_mellemlang_videregaaende', 'udd_bachelor',
                     'udd_lang_videregaaende', 'udd_forsker', 'udd_uoplyst',
                     'socio_high_selvst', 'socio_mellemniveau', 'socio_grundniveau', 'socio_ledig_kontant',
                     'socio_pensionist', 'socio_other', 'civilstand_ugift', 'civilstand_gift', 'civilstand_skilt',
                     'civilstand_enke', 'ssh_anden_hustype', 'ssh_enlig_m_born', 'ssh_enlig_u_born', 'ssh_par_m_born',
                     'ssh_par_u_born', 'latitude', 'longitude']:
            try:
                if Donation_data[cols].isna().sum() > 0:
                    Donation_data[cols].replace({np.nan: Donation_data[cols].mean()}, inplace=True)

            except:
                continue

        for cols in ['robinson', 'antal_beboere', 'husstandsindkomst', 'donation_ssh', 'donation_gns',
                     'antal_vaerelser', 'day', 'month', 'year', 'hour', 'minute', 'week_of_year', 'target_column']:
            try:
                if Donation_data[cols].isna().sum() > 0:
                    Donation_data[cols].replace({np.nan: Donation_data[cols].mean()}, inplace=True)

            except:
                continue

        return Donation_data
