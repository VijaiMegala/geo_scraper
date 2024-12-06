import hashlib
import json
from fastapi import APIRouter, HTTPException
from app.schemas import GeoFeature
from app.database import get_db_connection
from psycopg2.extras import RealDictCursor  
from shapely.geometry import shape
from shapely import wkt


router = APIRouter()

def generate_feature_id(feature):
    hash_input = str(feature.geometry) + str(feature.properties)
    return hashlib.md5(hash_input.encode()).hexdigest()

@router.get("/features/{feature_id}", response_model=GeoFeature)
async def get_feature(feature_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor) 
    cursor.execute("SELECT feature_id, properties, ST_AsText(geom) FROM geo_features WHERE feature_id = %s", (feature_id,))
    row = cursor.fetchone()
    print(row)
    cursor.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Feature not found")

    geometry = wkt.loads(row['st_astext'])
    geojson = {
        "type": "Feature",
        "geometry": geometry.__geo_interface__, 
        "properties": row['properties']
    }

    return geojson

@router.post("/features")
async def create_feature(feature: GeoFeature):
    
    
    geometry = shape(feature.geometry).wkt 
    properties = json.dumps(feature.properties)
    feature_id = generate_feature_id(feature)


    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
   
    cursor.execute("SELECT feature_id FROM geo_features WHERE feature_id = %s", (feature_id,))
    existing = cursor.fetchone()
    if existing:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Feature already exists with this feature_id")

    cursor.execute("""
            INSERT INTO geo_features (feature_id, properties, geom)
            VALUES (%s, %s, ST_GeomFromText(%s, 4326))
            ON CONFLICT (feature_id)
            DO UPDATE SET properties = EXCLUDED.properties, geom = EXCLUDED.geom
            WHERE geo_features.properties IS DISTINCT FROM EXCLUDED.properties;
        """, (feature_id, properties, geometry))
    conn.commit()
    cursor.close()
    conn.close()
    raise HTTPException(status_code=201, detail="Data Inserted Successfully")

@router.patch("/features/{feature_id}", response_model=GeoFeature)
async def patch_feature(feature_id: str, feature: GeoFeature):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)  

    cursor.execute("SELECT properties, ST_AsText(geom) FROM geo_features WHERE feature_id = %s", (feature_id,))
    existing = cursor.fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Feature not found")

    geometry = shape(feature.geometry).wkt 
    properties = json.dumps(feature.properties)
    print(properties)
    print(existing)
    updated_properties = properties or existing['properties']
    updated_geom = geometry if feature.geometry else existing['st_astext']

    cursor.execute("""
        UPDATE geo_features
        SET properties = %s, geom = ST_GeomFromText(%s, 4326)
        WHERE feature_id = %s
        RETURNING feature_id, properties, ST_AsText(geom);
    """, (updated_properties, updated_geom, feature_id))

    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    updated_geometry = wkt.loads(row['st_astext'])  
    geojson = {
        "type": "Feature",
        "geometry": updated_geometry.__geo_interface__, 
        "properties": row['properties']
    }

    return geojson

@router.delete("/features/{feature_id}")
async def delete_feature(feature_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM geo_features WHERE feature_id = %s", (feature_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Feature deleted successfully"}
