DECLARE @ClaimCount INT = 5;

UPDATE TOP (@ClaimCount) staging
SET state = 'running'
OUTPUT inserted.name
WHERE state = 'outstanding';

GO
