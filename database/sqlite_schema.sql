CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    country TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vapes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' TEXT,
    'type' TEXT
);

-- Main table that will link the user to their vape and nicotine concentration
--limit to 5 dif vapes per user
CREATE TABLE user_to_vape (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    vape_id INTEGER,
    nicotine_concentration_mg_per_ml INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, vape_id),
    FOREIGN KEY (vape_id) REFERENCES vapes(id)
);

CREATE TABLE vape_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    vape_id INTEGER,
    air_inhaled REAL,
    nicotine_concentration_mg_per_ml INT,
    total_nicotine_inhaled REAL,
    'date' DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE VIEW all_vape_history_view AS 
SELECT 
    users.first_name,
    users.last_name, 
    vapes.name AS vape_name,
    vapes.type,
    vape_history.air_inhaled,
    vape_history.nicotine_concentration_mg_per_ml,
    vape_history.total_nicotine_inhaled
FROM users 
JOIN vape_history ON users.id = vape_history.user_id
JOIN vapes ON vapes.id = vape_history.vape_id;


--testing data please delete later
INSERT INTO users(id, first_name, last_name, gender, country)
VALUES (1, 'francy', 'romelus', 'male', 'us');

INSERT INTO vapes(id, 'name', 'type')
VALUES (1, 'juul', 'pod');

INSERT INTO user_to_vape(id, user_id, vape_id, nicotine_concentration_mg_per_ml)
VALUES (1, 1, 1, 5);

INSERT INTO vape_history(id, user_id, vape_id, nicotine_concentration_mg_per_ml, air_inhaled, total_nicotine_inhaled)
VALUES (1, 1, 1, 5, 25, 100);