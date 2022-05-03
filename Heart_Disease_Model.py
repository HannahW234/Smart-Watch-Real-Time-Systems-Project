import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix,accuracy_score,roc_curve,classification_report


class Heart_Disease_Model:
    def __init__(self):
        self.data = self.get_data()
        self.svc = self.SVC_model()

    def get_data(self):
        data = pd.read_csv("./heart.csv")
        #feature engineering 
        data = data.drop(columns=['age','sex','cp','fbs','ca','thal','trestbps','chol','restecg','oldpeak','slope'])
        
        return data
    
    def SVC_model(self):
        y = self.data['target']
        X = self.data.drop('target',axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state = 0)
        
        svc1 =  SVC(kernel='rbf', C=2)
        svc1.fit(X_train, y_train)
        svc_predicted = svc1.predict(X_test)
        return svc1

    def predict_heart_disease(self, X_test): 
        y_pred = self.svc.predict([X_test])
        if y_pred == 1: 
            return True 
        return False 




