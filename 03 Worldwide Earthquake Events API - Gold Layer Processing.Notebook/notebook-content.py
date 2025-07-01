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
# META     },
# META     "environment": {
# META       "environmentId": "e00f6171-3059-a328-4ba3-9331864d68cd",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Worldwide Earthquake Events API - Gold Layer Processing

# CELL ********************

from pyspark.sql.functions import when, col, udf
from pyspark.sql.types import StringType
# ensure the below library is installed on your fabric environment
import reverse_geocoder as rg
from datetime import date

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# PARAMETERS CELL ********************

start_date = date.today()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print("Parameter start_date is ", start_date)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.table("earthquake_events_silver").filter(col('time') > start_date)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### Test reverse_geocoder

# CELL ********************

coordinates = (-122.771667480469, 38.7876663208008)

rg.search(coordinates)[0]
# rg.search(coordinates)[0].get('cc')     # 'cc' คือรหัสประเทศ 2 ตัว ซึ่งสามารถเอาไว้ใช้ใน Power BI ได้

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def get_country_code(lat, lon):
    """
    Retrieve the country code for a given latitude and longitude.

    Parameters:
    lat (float or str): Latitude of the location.
    lon (float or str): Longitude of the location.

    Returns:
    str: Country code of the location, retrieved using the reverse geocoding API.

    Example:
    >>> get_country_details(48.8588443, 2.2943506)
    'FR'
    """
    coordinates = (float(lat), float(lon))
    return rg.search(coordinates)[0].get('cc')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# registering the udfs so they can be used on spark dataframes
get_country_code_udf = udf(get_country_code, StringType())

# udf() ใน PySpark ย่อมาจาก User Defined Function หรือ ฟังก์ชันที่ผู้ใช้กำหนด 
# ซึ่งเป็นฟังก์ชันที่ผู้ใช้สร้างขึ้นเองเพื่อขยายความสามารถของ PySpark โดยเฉพาะ 
# UDF ช่วยให้สามารถนำตรรกะการประมวลผลข้อมูลที่กำหนดเองมาใช้ใน DataFrame หรือในการ query SQL ของ PySpark ได้ 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# adding country_code and city attributes
df_with_location = \
                df.\
                    withColumn("country_code", get_country_code_udf(col("latitude"), col("longitude")))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# adding significance classification
df_with_location_sig_class = \
                            df_with_location.\
                                withColumn('sig_class', 
                                            when(col("sig") < 100, "Low").\
                                            when((col("sig") >= 100) & (col("sig") < 500), "Moderate").\
                                            otherwise("High")
                                            )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# appending the data to the gold table
df_with_location_sig_class.write.mode('append').saveAsTable('earthquake_events_gold')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
