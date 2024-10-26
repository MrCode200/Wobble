INSERT INTO users (username, xp, lvl)
VALUES (:username, :xp, :lvl)
ON CONFLICT(username) DO UPDATE SET xp = excluded.xp, lvl = excluded.lvl;
