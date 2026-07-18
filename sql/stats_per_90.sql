SELECT name, total_goals, total_assists, total_minutes,
ROUND(total_goals/total_minutes*90, 3) AS goals_per_90, 
ROUND(total_assists/total_minutes*90, 3) AS assists_per_90
FROM players_fresh_stats
WHERE total_minutes >= 2000
ORDER BY goals_per_90 DESC 
LIMIT 10;