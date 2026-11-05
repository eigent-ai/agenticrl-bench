DECLARE @BatchSize INT = 100;

UPDATE TOP (@BatchSize) jobs
SET status = 'claimed'
WHERE status = 'pending';

GO
