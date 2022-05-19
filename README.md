![blocklook](blocklook-logo.svg?raw=true "blocklook")
---
BlockLook data app enables users to look at swaps, volumes and liquidity on DEX's over a custom date range.

First, we built API's to get DEX data from Covalent unified APIs (XY=K endpoints). Second, we transformed the data into widgets to see swaps made by supported DEX's on multiple blockchains, their liquidity pool and volume.

This data app prototype demonstrates how quick and easy it is to look at blockchain and DEX activity in a clean user-friendly way. This can be built further by introducing more on-chain and relevant off-chain market data, such as ranking and popularity.

Technology
---
Built using Python, a commonly used language for Data Science and Data Engineering. It uses Pandas for data transformation and Streamlit to build a simple data application. We get on-chain data using Covalent unified data API. For this prototype specifically XY=K endpoints.

Run Locally
---
 - Get [Covalent](https://www.covalenthq.com/platform/#/) API Key
 - Create secrets.toml under .streamlit and add the Covalent API key. See example in sample-secrets/secrets.toml
 - Run the blocklook data app
 
    ```streamlit run blocklook-app.py```
    
    This will launch the data application in your default browser.
    
References
---

- Covalent API docs: https://www.covalenthq.com/docs/api/#/0/0/USD/1

- Streamlit docs: https://docs.streamlit.io/
