class SensorReading:
    def __init__(self, sensor_id: str, value: float):
        self.sensor_id = sensor_id
        self.value = value

    def __repr__(self):
        return f"SensorReading(sensor_id={self.sensor_id!r}, value={self.value!r})"
