SELECT * FROM player_stats t
WHERE t.datetime = (SELECT MAX(datetime) FROM player_stats);
