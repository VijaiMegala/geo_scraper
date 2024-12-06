from sqlalchemy import Column, String, JSON
from geoalchemy2 import Geometry
from app.database import Base

class GeoFeature(Base):
    __tablename__ = "geo_features"
    feature_id = Column(String, primary_key=True, index=True)
    properties = Column(JSON, nullable=False)
    geom = Column(Geometry("POLYGON"), nullable=False)
