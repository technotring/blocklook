"""
Data Application showing Decentralised Exchange Data.
"""

from datetime import timedelta

import streamlit as st

from api import get_unique_chains, get_dexes_on_chain, get_30days_volume_liquidity

with st.container():
    st.markdown(f'<h1><br>Decentralised Exchange (DEX) <br> Trade Analysis</h1> <hr/>',
                unsafe_allow_html=True)
    row1_1, row1_2 = st.columns((1, 1))
    with row1_1:
        chainOption = st.selectbox(
            'Chain',
            get_unique_chains())
    with row1_2:
        dexOption = st.selectbox(
            'Decentralised Exchange (DEX)',
            get_dexes_on_chain(chainOption))

with st.container():
    st.markdown(f'<h2>On {chainOption} - {dexOption}</h2>', unsafe_allow_html=True)
    xyk_pool_df = get_30days_volume_liquidity(chainOption, dexOption)
    if xyk_pool_df.empty:
        st.text('Data is not available yet for this exchange.')
    else:
        start_date, end_date = st.select_slider(
            'Date range',
            options=xyk_pool_df[['date']],
            value=(xyk_pool_df['date'].max() - timedelta(days=6), xyk_pool_df['date'].max()))
        with st.container():
            st.markdown(
                f'<h3>{(end_date - start_date).days + 1} days trading '
                f'(from {start_date:%B %d, %Y} to {end_date:%B %d, %Y})</h3> ',
                unsafe_allow_html=True)
            filtered_df = xyk_pool_df[
                (xyk_pool_df['date'] >= start_date) & (xyk_pool_df['date'] <= end_date)] \
                .set_index('date')
            with st.container():
                st.markdown(f'<h4>Swaps</h4> ', unsafe_allow_html=True)
                st.line_chart(filtered_df[['swap_count_24']])
            with st.container():
                st.markdown(f'<h4>Liquidity vs Volume</h4> ', unsafe_allow_html=True)
                st.area_chart(filtered_df[['volume_quote', 'liquidity_quote']])
            with st.container():
                st.markdown(f'<h4>Exchange Pool Dataset</h4> ', unsafe_allow_html=True)
                st.dataframe(filtered_df.reset_index().style.highlight_max(axis=0))
