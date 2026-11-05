SELECT vehicleId, isConnected, MAX(lastUpdate) AS lastUpdate FROM vehicle_connection_status WHERE missionId=1 GROUP BY vehicleId;
