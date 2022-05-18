import configparser

import pandas as pd
import requests
import streamlit as st

"""
These APIs make requests to Covalent Unified XY=K endpoints and transforms the data to user's needs.
"""
configParser = configparser.RawConfigParser()
configFilePath = 'config/prod.cfg'
configParser.read(configFilePath)

covalent_xyk_api = 'https://api.covalenthq.com/v1'
payload = {'key': f'{configParser.get("blocklook", "covalent-apikey")}'}


def __pretty_print_df(df):
    with pd.option_context('display.max_rows', 50,
                           'display.max_columns', None,
                           'display.width', 1000,
                           'display.precision', 3,
                           'display.colheader_justify', 'center'):
        print(df)


@st.cache
def __get_supported_dexes():
    dexes_res = requests.get(f'{covalent_xyk_api}/xy=k/supported_dexes/', payload).json()
    dexes_df = pd.json_normalize(dexes_res['data'], ['items'])
    return dexes_df


@st.cache
def __get_chain_id(chain_name):
    chain_id_names = __get_supported_dexes().drop_duplicates(['chain_id'])
    chain_id_name_dict = dict(zip(chain_id_names['chain_name'], chain_id_names['chain_id']))
    return chain_id_name_dict[chain_name]


@st.cache
def __get_xyk_ecosystem(chain_name, dex_name):
    chain_id = __get_chain_id(chain_name)
    xyk_ecosystem_json = requests.get(f'{covalent_xyk_api}/{chain_id}/xy=k/{dex_name}/ecosystem/', payload).json()
    return xyk_ecosystem_json


@st.cache
def get_unique_chains():
    unique_by_chain_df = __get_supported_dexes().drop_duplicates(['chain_id'])
    return unique_by_chain_df['chain_name']


@st.cache
def get_dexes_on_chain(chain_name):
    supported_dexes_df = __get_supported_dexes()
    dexes_on_chain = supported_dexes_df[supported_dexes_df['chain_name'] == chain_name]['dex_name']
    return dexes_on_chain


@st.cache
def get_30days_volume_liquidity(chain_id, dex_name):
    xyk_eco_json = __get_xyk_ecosystem(chain_id, dex_name)
    volume_30d_df = pd.json_normalize(xyk_eco_json, ['data', 'items', 'volume_chart_30d'])
    liquidity_30d_df = pd.json_normalize(xyk_eco_json, ['data', 'items', 'liquidity_chart_30d'])
    merged_7days_result = pd.merge(volume_30d_df, liquidity_30d_df, "inner",
                                   ['dt', 'chain_id', 'dex_name', 'quote_currency'])
    merged_7days_result['date'] = pd.to_datetime(merged_7days_result['dt']).dt.date
    result = merged_7days_result[['date', 'swap_count_24', 'volume_quote', 'liquidity_quote']]
    return result
