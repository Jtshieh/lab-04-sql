-- Popular posts by members interested in science or technology.
SELECT p.post_id, u.username, u.interest, p.title, p.likes
FROM posts AS p
JOIN users AS u ON p.user_id = u.user_id
WHERE u.interest IN ('Science', 'Technology') AND p.likes >= 10
ORDER BY p.likes DESC, p.post_id;
