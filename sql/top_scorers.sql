SELECT p.player_id, p.name, s.total_goals, s.total_appearances
FROM players_fresh_final AS s JOIN players AS p ON s.player_id=p.player_id
ORDER BY s.total_goals DESC
LIMIT 10;