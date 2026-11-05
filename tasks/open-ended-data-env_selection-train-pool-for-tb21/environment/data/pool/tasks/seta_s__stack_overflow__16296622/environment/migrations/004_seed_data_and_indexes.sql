SET NOCOUNT ON;
GO

-- Create indexes
CREATE INDEX [IX_Users_Email] ON [Users] ([Email]);
GO
CREATE INDEX [IX_Orders_UserID] ON [Orders] ([UserID]);
GO
CREATE INDEX [IX_Categories_Name] ON [Categories] ([CategoryName]);
GO

-- Seed users
INSERT INTO [Users] ([FirstName], [LastName], [Email], [Active], [CreatedDate], [ProfileGUID])
VALUES (N'Alice', N'Smith', N'alice@example.com', 1, '2024-01-15 10:30:00', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');
GO
INSERT INTO [Users] ([FirstName], [LastName], [Email], [Active], [CreatedDate], [ProfileGUID])
VALUES (N'Bob', N'Jones', N'bob@example.com', 1, '2024-02-20 14:45:00', 'b2c3d4e5-f6a7-8901-bcde-f12345678901');
GO
INSERT INTO [Users] ([FirstName], [LastName], [Email], [Active], [CreatedDate], [ProfileGUID])
VALUES (N'Charlie', N'Brown', N'charlie@example.com', 0, '2024-03-10 09:00:00', 'c3d4e5f6-a7b8-9012-cdef-123456789012');
GO

-- Seed categories
INSERT INTO [Categories] ([CategoryName], [ParentCategoryID], [Visible], [Description])
VALUES (N'Electronics', NULL, 1, N'Electronic devices and accessories');
GO
INSERT INTO [Categories] ([CategoryName], [ParentCategoryID], [Visible], [Description])
VALUES (N'Books', NULL, 1, N'Physical and digital books');
GO
INSERT INTO [Categories] ([CategoryName], [ParentCategoryID], [Visible], [Description])
VALUES (N'Electronics - Phones', 1, 1, N'Mobile phones and accessories');
GO

-- Seed orders
INSERT INTO [Orders] ([UserID], [TotalAmount], [Status], [OrderDate])
VALUES (1, 299.99, N'Completed', '2024-03-01 16:20:00');
GO
INSERT INTO [Orders] ([UserID], [TotalAmount], [Status], [OrderDate])
VALUES (1, 49.50, N'Pending', '2024-03-15 11:00:00');
GO
INSERT INTO [Orders] ([UserID], [TotalAmount], [Status], [OrderDate])
VALUES (2, 150.00, N'Shipped', '2024-03-10 08:30:00');
GO

PRINT 'Migration 004 complete: indexes and seed data added.'
GO
