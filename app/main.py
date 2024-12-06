from fastapi import FastAPI
from app.routes.geo_features import router as geo_features_router

app = FastAPI(title="GeoJSON CRUD API")

app.include_router(geo_features_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
