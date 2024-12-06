# CRED Operations with FastAPI and PostgreSQL

## Project Overview
This is a CRED (Create, Read, Update, Delete) operations project built using FastAPI, PostgreSQL, and Docker.

## Prerequisites
- Docker
- Docker Compose

## Configuration

### Database Hostname
To connect to the database using your local IP:

1. Open the `docker-compose.yml` file
2. Locate the database service configuration
3. Replace `hostname: db` with your local IP address

Example:
```yaml
services:
  db:
    hostname: 192.168.1.100  # Replace with your actual IP
```

## Getting Started

### Installation
1. Clone the repository
2. Update database hostname in `docker-compose.yml`
3. Start the application:

<!-- bash -->
docker compose up

This command will automatically build the Docker images and start the containers.

## API Endpoints

### Feature Operations
The application supports the following operations on features:

 ## Create a Feature
- **Method**: POST
- **URL**: `http://localhost:8000/api/v1/features`
- **Request Body Example**:

## json
{
    "type": "Feature",
    "properties": {
        "fill": "#00f"
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [75.09160410950545, 16.810177981518162],
                ... (coordinate list)
            ]
        ]
    }
}


#### Read a Feature
- **Method**: GET
- **URL**: `http://localhost:8000/api/v1/features/{feature_id}`
- **Example**: `http://localhost:8000/api/v1/features/5efe311e6a1ebd30df4e2711ef1c1439`

#### Update a Feature
- **Method**: PATCH
- **URL**: `http://localhost:8000/api/v1/features/{feature_id}`
- **Request Body Example**:
## json
{
    "type": "Feature",
    "properties": {
        "fill": "#ff0001"
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            ... (updated coordinate list)
        ]
    }
}


#### Delete a Feature
- **Method**: DELETE
- **URL**: `http://localhost:8000/api/v1/features/{feature_id}`

## Testing Workflow
1. Create a feature using the POST endpoint
2. Retrieve the feature using the GET endpoint with the returned ID
3. Update the feature using the PATCH endpoint
4. Verify the update by getting the feature again
5. Delete the feature using the DELETE endpoint
6. Confirm deletion by attempting to get the feature (should return a 404 error)

## Tools for Testing
- Postman
- cURL
- Any API testing tool that supports HTTP requests

## Notes
- Ensure Docker is running before starting the application
- The application runs on `http://localhost:8000`
- All endpoints are prefixed with `/api/v1/features`