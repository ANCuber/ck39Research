--@block
SHOW DATABASES


--@block
INSERT INTO data(latex) VALUE ("\\frac{2}{3}");



--@block
SELECT * from data

--@block
SELECT * from data WHERE done=0 ORDER BY RAND() LIMIT 1

--@block
UPDATE DATA
SET description='哈摟'
WHERE id=1

--@block
DELETE FROM data