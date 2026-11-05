package main

import (
	"encoding/csv"
	"os"
	"strconv"
)

type SensorReading struct {
	ID        int
	Name      string
	Location  string
	Value     float64
	Timestamp string
}

func ReadSensors(path string) ([]SensorReading, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	reader := csv.NewReader(f)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	var sensors []SensorReading
	for _, rec := range records[1:] { // skip header
		id, _ := strconv.Atoi(rec[0])
		val, _ := strconv.ParseFloat(rec[3], 64)
		sensors = append(sensors, SensorReading{
			ID:        id,
			Name:      rec[1],
			Location:  rec[2],
			Value:     val,
			Timestamp: rec[4],
		})
	}
	return sensors, nil
}
