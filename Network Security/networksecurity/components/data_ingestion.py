from networksecurity.exception import NetworkSecurityException
from networksecurity.logger import logging

## configuration of data ingestion config

from networksecurity.entity.config_entity import DataIngestionConfig
import os
import sys
import numpy as np
import pymongo
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL= os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_dataframe(self):
        """read data from mongodb"""
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client= pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({ "na": np.nan}, inplace= True)
            return df
        except Exception as e:
            raise NetworkSecurityException
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
        except:
            raise NetworkSecurityException
        
    
