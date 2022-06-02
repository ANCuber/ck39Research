--@block
SHOW DATABASES


--@block
INSERT INTO data(latex) VALUE ("orz");


--@block
SELECT * from data WHERE done=1


--@block
SELECT * from data WHERE id=1
ORDER BY done DESC

--@block
DELETE FROM data WHERE description IS NULL;



--@block
UPDATE DATA SET done=0 WHERE id=901;





--@block

SELECT COUNT(*) FROM data WHERE done=1
--@block

SELECT COUNT(*) FROM data