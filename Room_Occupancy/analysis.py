from sklearn import metrics
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import datetime
import pandas as pd
import numpy as np

SCALER = StandardScaler()
TRAIN_SIZE = 0.75
TEST_SIZE = 0.25
TEMP_MEAS = [f'S{i + 1}_Temp' for i in range(4)]
LIGHT_MEAS = [f'S{i + 1}_Light' for i in range(4)]
SOUND_MEAS = [f'S{i + 1}_Sound' for i in range(4)]
MEASUREMENTS_COLUMNS_GROUPS = [TEMP_MEAS, LIGHT_MEAS, SOUND_MEAS]
MEASUREMENTS_STRINGS = ["Temperature", "Light", "Sound"]
OTHER_PREDICTORS = ['S5_CO2', 'S5_CO2_Slope', 'S6_PIR', 'S7_PIR']
PREDICTORS = TEMP_MEAS + LIGHT_MEAS + SOUND_MEAS + OTHER_PREDICTORS
LABEL = 'Room_Occupancy_Count'
PREDICTION = 'Room_Occupancy_Count_Pred'
D_HYPERPARAMETERS = {
    'RANDOM_FOREST': {"n_trees": 30, 'min_samples_leaf': 30}
}
DATETIME = 'FULL_DATETIME'
SENSORS_COLORS = ['navy', 'cyan', 'red', 'pink']

if __name__ == '__main__':
    df = pd.read_csv(r'.\data\Occupancy_Estimation.csv')
    X_org = df[PREDICTORS].values
    # X_agg = np.concatenate([df[col].mean(axis=1).values[:, None] for col in [TEMP_MEAS, LIGHT_MEAS, SOUND_MEAS]], 1)
    # X_new = np.concatenate([X_agg, df[OTHER_PREDICTORS].values], 1)
    X_new = X_org
    X = SCALER.fit_transform(X_new)
    y = df[LABEL].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, shuffle=False
    )

    d_hyper = D_HYPERPARAMETERS['RANDOM_FOREST']
    random_forest = RandomForestClassifier(n_estimators=d_hyper['n_trees'], min_samples_leaf=d_hyper['min_samples_leaf'])
    qda = QuadraticDiscriminantAnalysis()

    for model, model_string in zip([random_forest, qda], ['Random Forest', 'QDA']):
        model.fit(X_train, y_train)
        y_test_pred = model.predict(X_test)
        f1 = metrics.f1_score(y_test, y_test_pred, average='macro')
        f1 = round(100 * f1, 2)
        print(f'{model_string} Model test f1 score: {f1} %')

    df[PREDICTION] = qda.predict(X)
    df[DATETIME] = df.apply(lambda row: datetime.datetime.strptime(row['Date'] + ' ' + row['Time'], '%Y/%m/%d %H:%M:%S'), axis=1)
    df.to_csv(r'.\data\Occupancy_Estimation_Prediction.csv')

    smote = SMOTE(random_state=42)
    X_balanced, y_balanced = smote.fit_resample(X_train, y_train)
    for model, model_string in zip([random_forest, qda], ['Random Forest', 'QDA']):
        model.fit(X_balanced, y_balanced)
        y_test_pred = model.predict(X_test)
        f1 = metrics.f1_score(y_test, y_test_pred, average='macro')
        f1 = round(100 * f1, 2)
        print(f'{model_string} [training on a balanced dataset] Model test f1 score: {f1} %')
