WITH stats AS (
    SELECT player_id, competition_id, SUM(minutes_played) AS total_minutes
    FROM appearances 
        JOIN competitions USING("competition_id") 
        JOIN players_fresh_final USING("player_id")
    WHERE "type" = 'domestic_league'
        AND "date" <= "current_date"
        AND "date" >= date("current_date", '-365 days')
    GROUP BY 1, 2),
    ranked AS (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY total_minutes DESC) AS rank_num
        FROM stats
    )

SELECT player_id, competition_id AS main_league, total_minutes
FROM ranked
WHERE rank_num = 1