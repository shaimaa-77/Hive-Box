from fastapi import FastAPI
from fastapi import APIRouter
import requests
from constants import OPEN_SENSE_API_URL
import sys
import toml

def get_app_version():
    try:
        with open("pyproject.toml", "r", encoding="utf-8") as file:
            config = toml.load(file)
        app_version = config.get("tool", {}).get("poetry", {}).get("version", "unknown version")
        return app_version
    except FileNotFoundError:
        return "pyproject.toml not found"
    

def get_temperature_of_sense_id(sensor_id):
    try:
        url = f"{OPEN_SENSE_API_URL}/boxes/{sensor_id}"
        response = requests.get(url, timeout=500)
        response.raise_for_status()
        data = response.json()
        
        if "sensors" not in data:
            print(f"No sensors found in response for {sensor_id}", file=sys.stderr)
            return 0
            
        for sensor in data.get("sensors", []):
            if sensor.get("title") == "Temperatur":
                last_measurement = sensor.get("lastMeasurement")
                if last_measurement and "value" in last_measurement:
                    return float(last_measurement["value"])
                print(f"No valid measurement found for temperature sensor in {sensor_id}", file=sys.stderr)
                return 0
                
        print(f"No temperature sensor found for {sensor_id}", file=sys.stderr)
        return 0
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for sensor {sensor_id}: {e}", file=sys.stderr)
        return 0
    except (ValueError, TypeError) as e:
        print(f"Error processing data for sensor {sensor_id}: {e}", file=sys.stderr)
        return 0
    

# Create the FastAPI app instance
app = FastAPI(
    title="Hive Box",
    description="Hive Box project",
    version=get_app_version(),
)

# Create router for temperature endpoints
temperature_router = APIRouter(tags=["Temperature"])

@app.get("/version")
async def get_version():
    return {"version": get_app_version()}

@temperature_router.get("/temperature")
async def get_box_temperature():
    sensor_ids = [
        "5eba5fbad46fb8001b799786",
        "5eb99cacd46fb8001b2ce04c",
        "5e60cf5557703e001bdae7f8",
    ]
    
    try:
        temperatures = [get_temperature_of_sense_id(ID) for ID in sensor_ids]
        valid_temperatures = [t for t in temperatures if t != 0]
        
        if not valid_temperatures:
            return {"error": "No valid temperature readings available"}
            
        average_temperature = round(sum(valid_temperatures) / len(valid_temperatures), 2)
        
        return {
            "average_temperature": average_temperature,
            "sensor_count": len(valid_temperatures),
            "total_sensors": len(sensor_ids)
        }
    except Exception as e:
        print(f"Error processing temperatures: {e}", file=sys.stderr)
        return {"error": str(e)}

# Include the temperature router
app.include_router(temperature_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    