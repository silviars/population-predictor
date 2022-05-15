import json
from collections import OrderedDict

import numpy as np
import pandas as pd
import queue as q
from sklearn.linear_model import LinearRegression

from predictor.models import Country


CSV_PATH = 'predictor/data/population.csv'
COUNTRIES_LIST_PATH = 'predictor/data/countries.json'
PQ_LIMIT = 20


def select_country(df, country):
    df = df.loc[df['country_name'] == country]
    df.drop(['country_name', 'Country Code', 'Indicator Name', 'Indicator Code'], axis=1, inplace=True)
    df = df.T
    df.dropna(inplace=True)
    df = df.reset_index()
    df.replace(np.nan, 0)
    return df


def fit_model(df):
    x = df.iloc[:, 0].values.reshape(-1, 1)
    y = df.iloc[:, 1].values.reshape(-1, 1)
    model = LinearRegression().fit(x, y)
    return model


def predict_population(model, year):
    population = model.predict([[year]])
    return int(population[0][0])


def reformat_data(df):
    df.rename(columns={'Country Name': 'country_name'}, inplace=True)
    df['country_name'] = df['country_name'].apply(lambda row: row.lower())
    return df


def format_result_list(pq):
    result_dict = {}
    i = PQ_LIMIT

    while not pq.empty():
        next_country = pq.get()
        result_dict[i] = next_country.name
        i -= 1

    res = OrderedDict(reversed(list(result_dict.items())))

    return res


def expected_population(country, year):
    df = pd.read_csv(CSV_PATH)
    df_formatted = reformat_data(df)

    with open(COUNTRIES_LIST_PATH) as f:
        country_list = json.load(f)

    country = country.lower()
    print(country)

    if country in country_list:
        df_country = select_country(df_formatted, country)
        if df_country.empty:
            return None

        model = fit_model(df_country)
        population = predict_population(model, year)

        return Country(country, year, population)

    return None


def top_n_populated(year):
    with open(COUNTRIES_LIST_PATH) as f:
        country_list = json.load(f)

    countries = q.PriorityQueue(maxsize=PQ_LIMIT + 1)

    for country in country_list:
        country_result = expected_population(country, year)

        if country_result is not None:
            countries.put(country_result)

        if countries.qsize() == countries.maxsize:
            countries.get()

    res = format_result_list(countries)

    return res
