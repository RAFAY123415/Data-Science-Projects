from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC
from time import perf_counter
from sklearn.metrics import precision_score
import pandas as pd


class DataModelling:

    def Data_Modelling(self, X_train, y_train):
        models = {
            "Random Forest": {"model": RandomForestClassifier(), "perf": 0},
            "Gradient Boosting": {"model": GradientBoostingClassifier(), "perf": 0},
            "XGBoost": {"model": XGBClassifier(eval_metric='mlogloss'), "perf": 0},
            "Logistic Regr.": {"model": LogisticRegression(), "perf": 0},
            "KNN": {"model": KNeighborsClassifier(), "perf": 0},
            "Decision Tree": {"model": DecisionTreeClassifier(), "perf": 0},
            "SVM (Linear)": {"model": LinearSVC(), "perf": 0},
            "Bagging Classifier": {"model": BaggingClassifier(), "perf": 0},}

        for name, model in models.items():
            start = perf_counter()
            model['model'].fit(X_train, y_train)
            duration = perf_counter() - start
            duration = round(duration, 2)
            model["perf"] = duration

        return models

    def Prediction_Score(self, X_test, y_test, models):
        models_acc = []
        for name, model in models.items():
            Name = name
            Y_pred = model['model'].predict(X_test)
            Precision = precision_score(y_test, Y_pred, average='binary')
            Accuracy = model["model"].score(X_test, y_test)
            Pref = model["perf"]
            Model_object = model["model"]
            models_acc.append([Name, Accuracy, Precision, Pref, Model_object])
        df_acc = pd.DataFrame(models_acc)
        df_acc.columns = ['Model', 'Accuracy w/o scaling', 'Precision', 'Training time (sec)', 'Model_Object']
        df_acc.sort_values(by='Precision', ascending=False, inplace=True)
        df_acc.reset_index(drop=True, inplace=True)
        best_Model_Based_on_Precision = df_acc.iloc[0][0]
        best_Accuracy_Score_based_on_Precision = df_acc.iloc[0][1]
        best_Precision_Score = df_acc.iloc[0][2]
        Training_time = df_acc.iloc[0][3]
        Model_Object = df_acc.iloc[0][4]

        return best_Model_Based_on_Precision, best_Accuracy_Score_based_on_Precision, best_Precision_Score, Training_time, Model_Object
