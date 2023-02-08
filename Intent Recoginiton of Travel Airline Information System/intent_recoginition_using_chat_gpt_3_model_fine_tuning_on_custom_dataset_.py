# -*- coding: utf-8 -*-
"""Intent Recoginition Using Chat Gpt-3 Model Fine Tuning on Custom Dataset .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SKEapvFFpm8zv-tsyjdWkpWULwJGMWZK

### Intent Recoginiton of Travel Airline Information System

### Fine tune Chat gpt On Intent Classification
"""

import pandas as pd
import numpy as np
np.random.seed(0)

"""#### Importing dataset"""

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv("/content/drive/MyDrive/Chat GPT Projects/atis_intents.csv",header=None)

"""#### Rename the column names """

data.columns = ['intent','text']

data['intent'].unique()

data['intent'].nunique()

"""## Replace the column value"""

data['intent'] = data['intent'].str.replace('#','_')

data['intent'] = data['intent'].str.replace('atis_','')

data['intent'].unique()

data['intent'].value_counts()

labels = ['flight','ground_service','airfare','abbreviation','flight_time']

data = data[data["intent"].isin(labels)]

data['intent'].value_counts()

"""#### Take only 40 samples of each target column """

sample_data = data.groupby('intent').apply(lambda x: x.sample(n=40)).reset_index(drop = True)

sample_data = sample_data[['text','intent']]

sample_data['text'] = sample_data['text'].str.strip()
sample_data['intent'] = sample_data['intent'].str.strip()

"""### The text goes into a standard way for fine tune a model ."""

sample_data['text'] = sample_data['text'] + "\n\nIntent:\n\n"
# sample_data['text'] = "Classify text into on the intent: flight, ground_service, airline, aircraft, flight_time. Text: "+sample_data['text'] + "\n\nIntent:\n\n"
sample_data['intent'] = " "+sample_data['intent'] + " END"

sample_data.head(2)

print(sample_data['text'][0])

print(sample_data['intent'][0])

sample_data.columns = ['prompt','completion']

!pip install openai==0.25.0

sample_data.to_json("intent_sample.jsonl", orient='records', lines=True)

!openai tools fine_tunes.prepare_data -f intent_sample.jsonl

import os
os.environ['OPENAI_API_KEY'] = "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"

!openai api fine_tunes.create -t "intent_sample_prepared_train.jsonl" -v "intent_sample_prepared_valid.jsonl" -m 'ada'

!openai api fine_tunes.follow -i ft-MRq1mcHHX4zcnBvjbqMvGoQo

!openai api fine_tunes.list

# prompt = "Do we have london flight on Monday\n\nIntent:\n\n"
# prompt = "what is the ap57 restriction\n\nIntent:\n\n"
prompt = "Do we have a london flight on Monday\n\nIntent:\n\n"

!pip install openai

import openai
openai.api_key ='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'
response = openai.Completion.create(
  model="ada:ft-personal-2023-02-07-14-10-09",
  prompt=prompt,
  max_tokens=5,
  temperature=0,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  stop=["END"]
)
print(response['choices'][0]['text'])