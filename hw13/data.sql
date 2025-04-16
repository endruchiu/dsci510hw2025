
INSERT INTO artists (name, genre) VALUES
('The Cosmic Keys', 'Rock'),
('Jazz Jaguars', 'Jazz'),
('Electro Ensemble', 'Electronic'),
('Folklore Friends', 'Folk'),
('Reggae Revolution', 'Reggae'),
('Classical Quintet', 'Classical'),
('Blues Brothers', 'Blues'),
('Pop Parade', 'Pop'),
('Metal Mavericks', 'Metal'),
('Country Cousins', 'Country');

INSERT INTO stages (name, location) VALUES
('Main Stage', 'Central Field'),
('Jazz Corner', 'North Wing'),
('Electronic Dome', 'East Field'),
('Folk Forest', 'West Woods'),
('Classical Hall', 'South Side'),
('Blues Bar', 'Near Entrance'),
('Pop Platform', 'Central Field'),
('Metal Mountain', 'North Hill'),
('Country Corner', 'West Woods'),
('Reggae Room', 'East Field');

INSERT INTO performances (artist_id, stage_id, start_time, end_time) VALUES
(1, 1, '2023-07-04 12:00', '2023-07-04 14:00'),
(2, 2, '2023-07-04 12:30', '2023-07-04 14:30'),
(3, 3, '2023-07-04 15:00', '2023-07-04 17:00'),
(4, 4, '2023-07-04 15:30', '2023-07-04 17:30'),
(5, 10, '2023-07-04 16:00', '2023-07-04 18:00'),
(6, 5, '2023-07-04 18:00', '2023-07-04 20:00'),
(7, 6, '2023-07-04 18:30', '2023-07-04 20:30'),
(8, 7, '2023-07-04 21:00', '2023-07-04 23:00'),
(9, 8, '2023-07-04 21:30', '2023-07-04 23:30'),
(10, 9, '2023-07-04 19:00', '2023-07-04 21:00');

INSERT INTO tickets (purchaser_name, purchase_date, price) VALUES
('Alex Smith', '2023-06-01', 59.99),
('Jamie Doe', '2023-06-02', 79.99),
('Sam Rivera', '2023-06-03', 49.99),
('Chris Green', '2023-06-04', 89.99),
('Pat Jordan', '2023-06-05', 99.99),
('Morgan Casey', '2023-06-06', 39.99),
('Taylor Swift', '2023-06-07', 109.99),
('Jordan Lee', '2023-06-08', 69.99),
('Casey Smith', '2023-06-09', 59.99),
('Riley Brown', '2023-06-10', 79.99);
