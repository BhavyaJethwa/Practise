import os
import sys
from src.MLproject.exception import CustonException
from src.MLproject.logger import logging
import pandas as pd
from dotenv import load_dotenv
import pymysql
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import pymysql


load_dotenv()

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

def read_sql_data():
    logging.info("Reading Started")
    try:
        mydb = pymysql.connect(
            host = host,
            user = user,    
            password=password,
            db = db
        )

        logging.info("Connection Successful" , mydb)
        df = pd.read_sql_query('select * from students' , mydb)
        print(df.head())

        return df


    except Exception as e:
        raise CustonException(e)
    
import pickle

def save_object(file_path , obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path , exist_ok=True)

        with open(file_path , "wb") as file_obj:
            pickle.dump(obj , file_obj)


    except Exception as e:
        raise CustonException(e,sys)
    

def evaluate_model(x_train , y_train , x_test , y_test , models , params):
    try:
        report = {}

        for i in range(len(list(models))):

            model = list(models.values())[i]

            para = params[list(models.keys())[i]]

            gs = GridSearchCV(model , para , cv=3)
            gs.fit(x_train , y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train , y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train , y_train_pred)
            test_model_score = r2_score(y_test , y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        
        return report

    except Exception as e:
        raise CustonException(e,sys)