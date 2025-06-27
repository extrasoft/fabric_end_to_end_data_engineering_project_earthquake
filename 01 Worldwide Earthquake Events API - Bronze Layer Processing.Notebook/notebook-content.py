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

# MARKDOWN ********************

# # <mark></mark>Worldwide Earthquake Events API - Bronze Layer Processing

# MARKDOWN ********************

# #### Initial default parameters

# CELL ********************

from datetime import date, timedelta

# start_date = previous 7 days
# end_date = yesterday
start_date = date.today() - timedelta(7) 
end_date = date.today() - timedelta(1) 

# url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"
# print(url)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Get response from Earthquake API then load into lakehouse

# CELL ********************

import requests
import json

# Construct the API URL with start and end dates provided by Data Factory, formatted for geojson output.
url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"

# Make the GET request to fetch data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Get the JSON response
    data = response.json()
    data = data['features']
    
    # Specify the file name (and path if needed)
    file_path = f'/lakehouse/default/Files/{start_date}_earthquake_data.json'

    # Open the file in write mode ('w') and save the JSON data
    # เปิดไฟล์ใน Lakehouse ตาม file_path 
    # 'w' = ถ้าไฟล์มีอยู่แล้ว "เขียนทับ" ถ้ายังไม่มี "สร้างไหม่"abs
    # indent=4 คือ ตอนเขียนไฟล์ .json ลง lakehouse ให้เนื้อหามีแถบเยื้อง = 4 เพื่อให้อ่านง่ายสวยงาม
    with open(file_path, 'w') as file:
        # The `json.dump` method serializes `data` as a JSON formatted stream to `file`
        # `indent=4` makes the file human-readable by adding whitespace
        json.dump(data, file, indent=4)
        
    print(f"Data successfully saved to {file_path}")
else:
    print("Failed to fetch data. Status code:", response.status_code)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.option("multiline", "true").json(f"Files/{start_date}_earthquake_data.json")
# df now is a Spark DataFrame containing JSON data from "Files/{start_date}_earthquake_data.json".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
