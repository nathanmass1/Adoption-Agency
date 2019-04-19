"""This code file is just to play aroudn with the Petfinder API """
import requests
from secrets import PETFINDER_API_KEY, SECRET
from model import db, connect_db, Pet

URL = "https://api.petfinder.com/v2/animals"

headers = {
  'authorization':
  'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjVjNWNmYzhkYTQ3NTNmZTQ5OTQ5NWI0M2FhNjhjOWUwOTFjZjUzNzQ1ZjA4Y2QwN2ZiMzZjNDczYmFmNzg1ZGZmZjc1NmNhZTE2YzcwYmY1In0.eyJhdWQiOiJKWjNqQ1FNRVZEbHM5eU96bnZEeEh4QkZ1dDd2ekxIMnBzeUJTUFB3VG9xSTZ4M2wxbSIsImp0aSI6IjVjNWNmYzhkYTQ3NTNmZTQ5OTQ5NWI0M2FhNjhjOWUwOTFjZjUzNzQ1ZjA4Y2QwN2ZiMzZjNDczYmFmNzg1ZGZmZjc1NmNhZTE2YzcwYmY1IiwiaWF0IjoxNTU1NzE0MzI0LCJuYmYiOjE1NTU3MTQzMjQsImV4cCI6MTU1NTcxNzkyNCwic3ViIjoiIiwic2NvcGVzIjpbXX0.jg8cgrhIQ_VLQK7jTDgXIfJlx0F7ukHVn7yo7FUEKfCZj1vB9eaEAbq23UQCXzGlfZLVWMs6RK4HdrCN9RD5iiVcTjLM_UOiXcDuwr9G2xOrDLLgDRuttu-CPzgAqlbAZhgh5h_UnnHUJ7tnfHgf1oSLTBJBE9vrQH6TaYWpLP4vY92fUKb28QmyfRHGyABEWi-N_19GuwGTJLwui2ZkhDVQ-kstqcYvzPcKWRDrkKd5wmAHj3AXuoyU18jSkJa1wOKHqeTgFMsX992alk_hw-18vpLUyk6knYDpqu_Q0hXSne7oagcS4IvFMVUaLcXtHYzR1tYv6af7t_1mMBXlpA'
}

params = {
  'species': 'Dog',
  'limit' : 5,
  'sort' : 'random'
}

def get_pets(params):
  response = requests.get(URL, headers=headers, params=params)

  # Grabs an array of dog JSON dictionaries from the API
  dogs = response.json()['animals']

  list_doggies = []
  # Extracts the info we need
  for dog in dogs:
    name = dog['name']
    age = convert_age_to_number(dog['age'])
    species = dog['species']
    if len(dog['photos']) > 0:
      photo_url = dog['photos'][0]['small']
    else:
      photo_url = None

    notes = dog['description']

    doggy = {
        "name" : name,
        "age" : age,
        "species" : species,
        "photo_url" : photo_url,
        "notes" : notes
    }

    list_doggies.append(doggy)

    return list_doggies
      # Places it in our database



def convert_age_to_number(api_age):
  """ Converts the API's age into a valid number """
  api_age = api_age.lower()

  LOOKUP = {
    'baby' : 0,
    'young' : 2,
    'adult' : 8,
    'senior' : 12
  }

  return LOOKUP[api_age]


