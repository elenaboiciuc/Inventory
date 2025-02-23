# Inventory
An inventory management system that allows users to book and release items seamlessly, with admin privileges for enhanced control.

# !! users for testing !! #
user1, user2, user3, admin
password: test


# SQLITE3 Insert - Sample Data already loaded in the db
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (1, 101, 'Ski Boots - Salomon X Pro', '2025-02-01', 'OK', 'Free');
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (2, 102, 'Snowboard - Burton Custom', '2025-02-05', 'OK', 'Free');
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (3, 103, 'Ski Jacket - North Face', '2025-02-08', 'Damaged', 'Free');
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (4, 104, 'Ski Poles - Leki', '2025-02-10', 'OK', 'Free');
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (5, 105, 'Snow Goggles - Oakley', '2025-02-15', 'Sent for maintenance', 'Free');
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (6, 106, 'Snowboard Boots - Burton Moto', '2025-02-10', 'OK', 'Free');
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (7, 107, 'Ski Helmet - Giro', '2025-02-22', 'OK', 'Free');
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (8, 108, 'Ski Pants - Columbia', '2025-02-25', 'Damaged', 'Free');
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (9, 109, 'Snowboard Bindings - Union Force', '2025-03-01', 'OK', 'Free');
INSERT INTO Inventory (id, number, description, registration_date, status, booked) VALUES (10, 110, 'Ski Gloves - Hestra', '2025-03-05', 'OK', 'Free');

