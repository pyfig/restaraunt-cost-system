CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE dishes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    total_cost NUMERIC(10, 2) NOT NULL
);

CREATE TABLE dish_ingredients (
    id SERIAL PRIMARY KEY,
    dish_id INT REFERENCES dishes(id) ON DELETE CASCADE,
    ingredient_id INT REFERENCES ingredients(id),
    quantity NUMERIC(10, 2) NOT NULL
);
