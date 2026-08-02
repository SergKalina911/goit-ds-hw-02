-- 1. Завдання певного користувача (наприклад, user_id = 1)
SELECT * FROM tasks WHERE user_id = 1;

-- 2. Завдання зі статусом 'new'
SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name='new');

-- 3. Оновити статус завдання
UPDATE tasks SET status_id = (SELECT id FROM status WHERE name='in progress') WHERE id=2;

-- 4. Користувачі без завдань
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);

-- 5. Додати нове завдання (наприклад, для користувача з id=3)
INSERT INTO tasks(title, description, status_id, user_id)
VALUES ('New Task', 'Description here', 1, 3);

-- 6. Незавершені завдання
SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name='completed');

-- 7. Видалити завдання (наприклад, з id=5)
DELETE FROM tasks WHERE id=5;

-- 8. Користувачі з email LIKE
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- 9. Оновити ім’я користувача (наприклад, для користувача з id=1)
UPDATE users SET fullname='Updated Name' WHERE id=1;

-- 10. Кількість завдань за статусами
SELECT s.name, COUNT(t.id) FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name;

-- 11. Завдання користувачів з певним доменом
SELECT t.* FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com';

-- 12. Завдання без опису
SELECT * FROM tasks WHERE description IS NULL;

-- 13. Користувачі та їхні завдання 'in progress'
SELECT u.fullname, t.title FROM users u
JOIN tasks t ON u.id = t.user_id
JOIN status s ON t.status_id = s.id
WHERE s.name='in progress';

-- 14. Кількість завдань кожного користувача
SELECT u.fullname, COUNT(t.id) FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.fullname;
