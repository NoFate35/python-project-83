CREATE TABLE IF NOT EXISTS urls (
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar (255),
    created_at TIMESTAMP
);