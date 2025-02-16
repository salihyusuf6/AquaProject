use AquaMain;
CREATE TABLE teacher_info (
    ID INT PRIMARY KEY,
    teacher VARCHAR(100),
    password VARCHAR(100)
);
CREATE TABLE class_info (
    class VARCHAR(100),
    ip VARCHAR(50),
    currentPassword INT
);