pip install nltk scikit-learn praw apache-airflow pymongo bertopic

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pymongo import MongoClient
import praw
import pandas as pd

import re
import unicodedata
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
import logging
