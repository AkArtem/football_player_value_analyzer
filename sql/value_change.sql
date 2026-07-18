SELECT v.date, p.name, v.market_value_in_eur,
v.market_value_in_eur - COALESCE(
    LAG(v.market_value_in_eur) OVER(PARTITION BY p.name ORDER BY v.date),
    v.market_value_in_eur
) AS value_change
FROM player_valuations AS v JOIN players AS p ON v.player_id=p.player_id
WHERE v.player_id = 8198
ORDER BY v.date