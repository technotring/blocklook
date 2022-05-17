"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st

from analytics.api import get_unique_chains, get_dexes_on_chain

chainOption = st.selectbox(
    'Chain',
    get_unique_chains())

'Your Selected Chain: ', chainOption

dexOption = st.selectbox(
    'DEX',
    get_dexes_on_chain(chainOption))

'Your selected DEX: ', dexOption
