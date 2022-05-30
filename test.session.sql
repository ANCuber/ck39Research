--@block
SHOW DATABASES


--@block
INSERT INTO data(latex) VALUE ("x^3");



--@block
SELECT * from data

--@block
SELECT * from data WHERE done=0 ORDER BY RAND() LIMIT 1

--@block
UPDATE DATA
SET description='哈摟'
WHERE id=1

--@block
