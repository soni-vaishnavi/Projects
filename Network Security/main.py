from networksecurity.components.data_ingestion import DataIngestion

from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig


from networksecurity.exception import NetworkSecurityException
from networksecurity.logger import logging 


import sys

if __name__== '__main__':
    try:
        trainingpiplineconfig = TrainingPipelineConfig()
        dataingestionconfig =DataIngestionConfig(trainingpiplineconfig)
        data_ingestion= DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)
    except Exception as e:
        raise NetworkSecurityException(e , sys)