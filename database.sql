DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar (255),
    created_at TIMESTAMP
);