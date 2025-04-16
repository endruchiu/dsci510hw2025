
-- Query 1: Artists in Rock genre
SELECT name
FROM artists
WHERE genre = 'Rock';

-- Query 2: Total revenue from ticket sales
SELECT SUM(price)
FROM tickets;

-- Query 3: Number of performances per stage
SELECT s.name, COUNT(p.performance_id) as performance_count
FROM stages s
LEFT JOIN performances p ON s.stage_id = p.stage_id
GROUP BY s.stage_id, s.name;

-- Query 4: Performances on 2023-07-04
SELECT a.name, s.location, p.start_time, p.end_time
FROM performances p
JOIN artists a ON p.artist_id = a.artist_id
JOIN stages s ON p.stage_id = s.stage_id
WHERE DATE(p.start_time) = '2023-07-04';

-- Query 5: Artists with performances > 2 hours
SELECT DISTINCT a.name
FROM artists a
JOIN performances p ON a.artist_id = p.artist_id
WHERE (JULIANDAY(p.end_time) - JULIANDAY(p.start_time)) * 24 > 2;
