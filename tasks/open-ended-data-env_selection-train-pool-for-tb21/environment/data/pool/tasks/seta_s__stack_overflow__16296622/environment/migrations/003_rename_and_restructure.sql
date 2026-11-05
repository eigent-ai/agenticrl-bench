SET NOCOUNT ON;
GO

-- Rename ProductCategories table to Categories
EXEC sp_rename 'ProductCategories', 'Categories'
GO

-- Add a new column to the renamed table
ALTER TABLE [Categories] ADD [Description] NVARCHAR(MAX) NULL;
GO

-- Add a new column to Users
ALTER TABLE [Users] ADD [LastLoginDate] DATETIME2 NULL;
GO

PRINT 'Migration 003 complete: table renamed and new columns added.'
GO
