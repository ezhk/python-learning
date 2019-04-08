USE `SocialNetwork`;

-- id пользователя и имя
SELECT `id` FROM `users` WHERE `name` = 'Andrey';
SELECT `name` FROM `users`;

-- лайков получено
--   можно использовать COUNT, но в дальнейшем,
--   скорее всего, захотим показывать кто поставил лайки
SELECT * FROM `users_likes`
	INNER JOIN `users` ON `users_likes`.`to` = `users`.`id`
	WHERE `users_likes`.`to` = 1;

-- Лайков поставлено
SELECT COUNT(*) FROM `users_likes`
	INNER JOIN `users` ON `users_likes`.`from` = `users`.`id`
	WHERE `users`.`name` = 'Andrey';

-- Взаимные лайки для пользователя с id = 1
SELECT `users`.`id`, `users`.`name` FROM `users_likes`
	INNER JOIN `users` ON (`users_likes`.`to` = `users`.`id`)
WHERE (`to` , `from`) IN (
    SELECT `from`, `to` FROM `users_likes`
) AND `from` = 1;

-- Список тех, кто не поставили like пользователю 5 и поставили 4 И 1
SELECT * FROM `users_likes`
WHERE `from` NOT IN (
	SELECT `from` FROM `users_likes`
		WHERE `users_likes`.`to` = 5
	) AND (`users_likes`.`to` = 4 OR `users_likes`.`to` = 1);

-- Список тех, кто не поставили like пользователю 5 и поставили 4 И 1
BEGIN;
SET @dislikes := (
	SELECT `from` FROM `users_likes`
		WHERE `users_likes`.`to` = 1
);

SELECT t1.`from` FROM `users_likes` as t1
INNER JOIN (
	SELECT * FROM `users_likes`
		WHERE `from` NOT IN (@dislikes) AND `users_likes`.`to` = 4
) as t2 ON t1.`from` = t2.`from`
WHERE t1.`from` NOT IN (@dislikes) AND t1.`to` = 5
;

COMMIT;
