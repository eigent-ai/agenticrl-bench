SELECT m.match_id, m.team, g.goals
FROM matches m
INNER JOIN goals_scored g ON m.match_id = g.match_id AND m.team = g.team;
