# Oracle Migration Project

Database migration scripts for upgrading from Oracle 11g to 19c.

## Structure
- `migrations/` - Sequential migration scripts
- `procedures/` - Stored procedures
- `views/` - Database views
- `triggers/` - Database triggers
- `sql_configs/` - Configuration files
- `scripts/` - Deployment and utility scripts
- `reports/` - Generated reports

## Usage
Run migrations in order using the deployment script:
```
./scripts/deploy.sh production
```

## Audit
Run the audit script to check for deprecated view references:
```
./audit.sh
```
