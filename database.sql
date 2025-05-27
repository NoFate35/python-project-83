DROP TABLE IF EXISTS urls, url_checks;


CREATE TABLE urls (
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar (255),
    created_at DATE
);

CREATE TABLE url_checks (
	id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	url_id int REFERENCES urls(id),
	status_code varchar (10),
	h1 varchar (255),
	description text,
	created_at DATE
	);