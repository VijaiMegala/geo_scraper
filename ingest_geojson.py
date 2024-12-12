import requests
import psycopg2
import hashlib
import json
from shapely.geometry import shape

conn = psycopg2.connect(
    dbname="geospatial_data",
    user="postgres",
    password="psql369",
    host="192.168.0.101",
    port="5431"
)
cursor = conn.cursor()

def fetch_geojson(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def generate_feature_id(feature):
    hash_input = str(feature['geometry']) + str(feature['properties'])
    return hashlib.md5(hash_input.encode()).hexdigest()

def ingest_geojson(data):
    for feature in data['features']:
        geometry = shape(feature['geometry']).wkt 
        properties = json.dumps(feature['properties'])
        feature_id = generate_feature_id(feature)
        print(feature['geometry'])
        
        cursor.execute("""
            INSERT INTO geo_features (feature_id, properties, geom)
            VALUES (%s, %s, ST_GeomFromText(%s, 4326))
            ON CONFLICT (feature_id)
            DO UPDATE SET properties = EXCLUDED.properties, geom = EXCLUDED.geom
            WHERE geo_features.properties IS DISTINCT FROM EXCLUDED.properties;
        """, (feature_id, properties, geometry))
        
    conn.commit()

def main():
    url = 'https://file.notion.so/f/f/9301458a-f465-42d3-80eb-7c09bae15034/282d7ed4-5168-4e77-91be-59906c19f9f3/Map_(10).geojson?table=block&id=655f6883-c12c-4503-bd82-157ea8ee1571&spaceId=9301458a-f465-42d3-80eb-7c09bae15034&expirationTimestamp=1734026400000&signature=xfNwIDA8pijPnupHOyd__MQHSw4w3h4S0pWZO8-Pj2w&downloadName=karnataka.geojson'
    geojson_data = fetch_geojson(url)
    ingest_geojson(geojson_data)

if __name__ == "__main__":
    main()
