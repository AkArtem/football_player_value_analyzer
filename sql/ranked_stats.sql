SELECT name, total_goals, total_assists, total_minutes, position,
ROUND(total_goals*90.0/total_minutes, 3) AS goals_per_90, 
ROUND(total_assists*90.0/total_minutes, 3) AS assists_per_90,
RANK() OVER (PARTITION BY position ORDER BY ROUND(total_goals*90.0/total_minutes, 3) DESC) AS rank_by_position,
DENSE_RANK() OVER (PARTITION BY position ORDER BY ROUND(total_goals*90.0/total_minutes, 3) DESC) AS dense_rank_by_position
FROM players_fresh_final
WHERE total_minutes >= 2000
ORDER BY position, rank_by_position
LIMIT 40;