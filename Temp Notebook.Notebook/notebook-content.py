# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "5ad5b400-2657-4122-8f04-7495fade5720",
# META       "default_lakehouse_name": "earthquakes_lakehouse",
# META       "default_lakehouse_workspace_id": "45397e97-41aa-433a-96dd-aed0944b7878",
# META       "known_lakehouses": [
# META         {
# META           "id": "5ad5b400-2657-4122-8f04-7495fade5720"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests

# requests.get(url)
# requests.get(url).status_code

response = requests.get(url)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# response.json()
# response.json()['metadata']
response.json()['features'][0]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
