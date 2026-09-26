-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    country TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vapes table
CREATE TABLE vapes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    type TEXT
);

-- Junction table linking users to their vapes with nicotine concentration
-- Limit to 5 different vapes per user
CREATE TABLE user_to_vape (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    vape_id INTEGER REFERENCES vapes(id),
    nicotine_concentration_mg_per_ml INTEGER,
    UNIQUE(user_id, vape_id)
);

-- Add check constraint to limit 5 vapes per user
CREATE OR REPLACE FUNCTION check_vape_limit()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM user_to_vape WHERE user_id = NEW.user_id) >= 5 THEN
        RAISE EXCEPTION 'User cannot have more than 5 different vapes';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_vape_limit
    BEFORE INSERT ON user_to_vape
    FOR EACH ROW
    EXECUTE FUNCTION check_vape_limit();

-- Vape usage history table
CREATE TABLE vape_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    vape_id INTEGER REFERENCES vapes(id),
    air_inhaled REAL,
    nicotine_concentration_mg_per_ml INTEGER,
    total_nicotine_inhaled REAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- View to show all vape history with user and vape details
CREATE VIEW all_vape_history_view AS 
SELECT 
    users.first_name,
    users.last_name, 
    vapes.name AS vape_name,
    vapes.type,
    vape_history.air_inhaled,
    vape_history.nicotine_concentration_mg_per_ml,
    vape_history.total_nicotine_inhaled,
    vape_history.date
FROM users 
JOIN vape_history ON users.id = vape_history.user_id
JOIN vapes ON vapes.id = vape_history.vape_id;

-- Test data (remove in production)
INSERT INTO users(first_name, last_name, gender, country)
VALUES ('francy', 'romelus', 'male', 'us');

INSERT INTO vapes(name, type)
VALUES ('juul', 'pod');

INSERT INTO user_to_vape(user_id, vape_id, nicotine_concentration_mg_per_ml)
VALUES (1, 1, 5);

INSERT INTO vape_history(user_id, vape_id, nicotine_concentration_mg_per_ml, air_inhaled, total_nicotine_inhaled)
VALUES (1, 1, 5, 25, 100);