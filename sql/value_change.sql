SELECT v.date, p.name, v.market_value_in_eur,
v.market_value_in_eur - LAG(v.market_value_in_eur, 1, 0)
OVER(PARTITION BY p.name ORDER BY v.date) AS value_change
FROM player_valuations AS v JOIN players AS p ON v.player_id=p.player_id
WHERE v.player_id = 8198
ORDER BY v.date