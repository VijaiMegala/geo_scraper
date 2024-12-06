from pydantic import BaseModel
from typing import Dict, List, Union

class GeoFeature(BaseModel):
    type: str  
    properties: Dict[str, str]
    geometry: Dict[str, Union[str, List[List[List[float]]]]]
