-- Fictional members and posts for a campus discussion board.
-- Select your assigned media database in the client, not in this script.
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    interest VARCHAR(30) NOT NULL,
    joined_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(120) NOT NULL,
    content TEXT NOT NULL,
    published_at DATETIME NOT NULL,
    likes INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_lab04_posts_users FOREIGN KEY (user_id) REFERENCES users(user_id)
);

START TRANSACTION;
-- The no-op duplicate clauses let the same seed script run twice safely.
INSERT INTO users VALUES (1, 'avery', 'Science', '2026-09-01 09:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;
INSERT INTO users VALUES (2, 'blair', 'Arts', '2026-09-02 10:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;
INSERT INTO users VALUES (3, 'casey', 'Sports', '2026-09-03 11:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;
INSERT INTO users VALUES (4, 'devon', 'Technology', '2026-09-04 12:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;
INSERT INTO users VALUES (5, 'ellis', 'Science', '2026-09-05 13:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;
INSERT INTO users VALUES (6, 'frankie', 'Arts', '2026-09-06 14:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;
INSERT INTO users VALUES (7, 'gray', 'Technology', '2026-09-07 15:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;
INSERT INTO users VALUES (8, 'harper', 'Sports', '2026-09-08 16:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;
INSERT INTO users VALUES (9, 'indigo', 'Science', '2026-09-09 17:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;
INSERT INTO users VALUES (10, 'jules', 'Arts', '2026-09-10 18:00:00') ON DUPLICATE KEY UPDATE user_id = user_id;

INSERT INTO posts VALUES (1, 1, 'Astronomy night', 'Bring a telescope to the observing session.', '2026-09-15 19:00:00', 12) ON DUPLICATE KEY UPDATE post_id = post_id;
INSERT INTO posts VALUES (2, 2, 'Gallery visit', 'A group visit to the student exhibition.', '2026-09-16 10:00:00', 7) ON DUPLICATE KEY UPDATE post_id = post_id;
INSERT INTO posts VALUES (3, 3, 'Weekend soccer', 'Meet at the field for a friendly game.', '2026-09-17 11:00:00', 15) ON DUPLICATE KEY UPDATE post_id = post_id;
INSERT INTO posts VALUES (4, 4, 'SQL study group', 'Practice joins and foreign keys together.', '2026-09-18 12:00:00', 20) ON DUPLICATE KEY UPDATE post_id = post_id;
INSERT INTO posts VALUES (5, 5, 'Lab tour', 'See the new teaching laboratory.', '2026-09-19 13:00:00', 4) ON DUPLICATE KEY UPDATE post_id = post_id;
INSERT INTO posts VALUES (6, 6, 'Sketching outdoors', 'Bring a pencil and a sketchbook.', '2026-09-20 14:00:00', 9) ON DUPLICATE KEY UPDATE post_id = post_id;
INSERT INTO posts VALUES (7, 7, 'Python workshop', 'Build a small CSV cleaning script.', '2026-09-21 15:00:00', 18) ON DUPLICATE KEY UPDATE post_id = post_id;
INSERT INTO posts VALUES (8, 8, 'Morning run', 'An easy run before class.', '2026-09-22 07:00:00', 6) ON DUPLICATE KEY UPDATE post_id = post_id;
INSERT INTO posts VALUES (9, 9, 'Research poster tips', 'Discuss how to label a scientific figure.', '2026-09-23 17:00:00', 11) ON DUPLICATE KEY UPDATE post_id = post_id;
INSERT INTO posts VALUES (10, 10, 'Open mic evening', 'Share music and poetry with classmates.', '2026-09-24 18:00:00', 13) ON DUPLICATE KEY UPDATE post_id = post_id;
COMMIT;
