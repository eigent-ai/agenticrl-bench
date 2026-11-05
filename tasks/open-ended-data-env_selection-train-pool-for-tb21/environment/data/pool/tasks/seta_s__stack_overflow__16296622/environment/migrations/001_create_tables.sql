SET NOCOUNT ON;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
BEGIN
    CREATE TABLE [Users] (
        [UserID] INT IDENTITY(1,1) NOT NULL,
        [FirstName] NVARCHAR(100) NOT NULL,
        [LastName] NVARCHAR(100) NOT NULL,
        [EmailAddress] NVARCHAR(255) NOT NULL,
        [IsActive] BIT DEFAULT 1,
        [CreatedDate] DATETIME2 DEFAULT GETDATE(),
        [ProfileGUID] UNIQUEIDENTIFIER DEFAULT NEWID(),
        CONSTRAINT [PK_Users] PRIMARY KEY ([UserID])
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Orders')
BEGIN
    CREATE TABLE [Orders] (
        [OrderID] INT IDENTITY(1,1) NOT NULL,
        [UserID] INT NOT NULL,
        [OrderTotal] DECIMAL(10,2) NOT NULL,
        [OrderStatus] NVARCHAR(50) DEFAULT N'Pending',
        [OrderDate] DATETIME2 DEFAULT GETDATE(),
        CONSTRAINT [PK_Orders] PRIMARY KEY ([OrderID]),
        CONSTRAINT [FK_Orders_Users] FOREIGN KEY ([UserID]) REFERENCES [Users]([UserID])
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ProductCategories')
BEGIN
    CREATE TABLE [ProductCategories] (
        [CategoryID] INT IDENTITY(1,1) NOT NULL,
        [CategoryName] NVARCHAR(200) NOT NULL,
        [ParentCategoryID] INT NULL,
        [IsVisible] BIT DEFAULT 1,
        CONSTRAINT [PK_ProductCategories] PRIMARY KEY ([CategoryID])
    );
END
GO

PRINT 'Migration 001 complete: base tables created.'
GO
