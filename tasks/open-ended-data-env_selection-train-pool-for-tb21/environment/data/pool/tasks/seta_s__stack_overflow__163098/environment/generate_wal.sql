\c appdb

DO $$
BEGIN
    FOR i IN 1..50 LOOP
        UPDATE sensor_readings SET reading_value = random() * 1000;
        INSERT INTO sensor_readings (sensor_name, reading_value)
        SELECT 'bulk_sensor_' || (j % 10)::text, random() * 500
        FROM generate_series(1, 200) AS s(j);
    END LOOP;
END $$;

CHECKPOINT;
