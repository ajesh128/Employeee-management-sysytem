CREATE TABLE Employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK(length(name) <= 50),
    email TEXT NOT NULL UNIQUE CHECK(length(email) <= 100),
    age INTEGER NOT NULL,
    department TEXT NOT NULL
);
