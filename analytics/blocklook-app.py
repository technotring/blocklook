"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st

from analytics.api import get_unique_chains, get_dexes_on_chain, get_7days_volume_liquidity

chainOption = st.selectbox(
    'Chain',
    get_unique_chains())

'Your Selected Chain: ', chainOption

dexOption = st.selectbox(
    'DEX',
    get_dexes_on_chain(chainOption))

'Your selected DEX: ', dexOption

volume_liquidity_7days_df = get_7days_volume_liquidity(chainOption, dexOption)

st.area_chart(volume_liquidity_7days_df, width=500, height=500)
