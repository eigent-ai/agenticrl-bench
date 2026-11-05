SET NOCOUNT ON;
GO

-- Rename EmailAddress to Email in Users table
EXEC sp_RENAME 'Users.EmailAddress', 'Email', 'COLUMN'
GO

-- Rename IsActive to Active in Users table
EXEC sp_RENAME 'Users.IsActive', 'Active', 'COLUMN'
GO

-- Rename OrderTotal to TotalAmount in Orders table
EXEC sp_RENAME 'Orders.OrderTotal', 'TotalAmount', 'COLUMN'
GO

-- Rename OrderStatus to Status in Orders table
EXEC sp_RENAME 'Orders.OrderStatus', 'Status', 'COLUMN'
GO

-- Rename IsVisible to Visible in ProductCategories
EXEC sp_RENAME 'ProductCategories.IsVisible', 'Visible', 'COLUMN'
GO

PRINT 'Migration 002 complete: columns renamed.'
GO
