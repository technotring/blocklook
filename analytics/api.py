import pandas as pd
import requests
import streamlit as st

covalent_xyk_api = 'https://api.covalenthq.com/v1'
api_key = ''
payload = {'key': api_key}


def pretty_print_df(df):
    with pd.option_context('display.max_rows', 50,
                           'display.max_columns', None,
                           'display.width', 1000,
                           'display.precision', 3,
                           'display.colheader_justify', 'center'):
        print(df)


def get_supported_dexes():
    dexes_res = requests.get(f'{covalent_xyk_api}/xy=k/supported_dexes/', payload).json()
    dexes_df = pd.json_normalize(dexes_res['data'], ['items'])
    # pretty_print_df(dexes_df)
    return dexes_df


def get_xyk_ecosystem(chain_id, dex_name):
    xyk_ecosystem_json = requests.get(f'{covalent_xyk_api}/{chain_id}/xy=k/{dex_name}/ecosystem/', payload).json()
    return xyk_ecosystem_json


def get_7days_volume_liquidity(chain_id, dex_name):
    xyk_eco_json = get_xyk_ecosystem(chain_id, dex_name)
    volume_7d_df = pd.json_normalize(xyk_eco_json, ['data', 'items', 'volume_chart_7d'])
    liquidity_7d_df = pd.json_normalize(xyk_eco_json, ['data', 'items', 'liquidity_chart_7d'])
    merged_7days_result = pd.merge(volume_7d_df, liquidity_7d_df, "inner",
                                   ['dt', 'chain_id', 'dex_name', 'quote_currency'])
    # pretty_print_df(merged_7days_result)


get_7days_volume_liquidity('1', 'uniswap_v2')


@st.cache
def get_unique_chains():
    # print("get_unique_chains CALLED")
    unique_by_chain_df = get_supported_dexes().drop_duplicates(['chain_id'])
    return unique_by_chain_df['chain_name']


@st.cache
def get_dexes_on_chain(chain_name):
    supported_dexes_df = get_supported_dexes()
    dexes_on_chain = supported_dexes_df[supported_dexes_df['chain_name'] == chain_name]['dex_name']
    pretty_print_df(dexes_on_chain)
    return dexes_on_chain