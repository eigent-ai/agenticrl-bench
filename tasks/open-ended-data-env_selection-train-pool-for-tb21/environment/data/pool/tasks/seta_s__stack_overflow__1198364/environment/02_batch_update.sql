DECLARE @BatchSize INT = 500;
DECLARE @RowsAffected INT = 1;
DECLARE @BatchNum INT = 0;

WHILE @RowsAffected > 0
BEGIN
    UPDATE TOP (@BatchSize) work_items
    SET processed = 1
    WHERE processed = 0;

    SET @RowsAffected = @@ROWCOUNT;

    IF @RowsAffected > 0
    BEGIN
        SET @BatchNum = @BatchNum + 1;

        INSERT INTO batch_log (batch_num, rows_affected, completed_at)
        VALUES (@BatchNum, @RowsAffected, GETDATE());
    END
END

GO
