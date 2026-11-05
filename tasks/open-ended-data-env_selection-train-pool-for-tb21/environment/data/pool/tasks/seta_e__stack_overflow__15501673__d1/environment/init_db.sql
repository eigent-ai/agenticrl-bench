CREATE OR REPLACE VIEW org_profile_view AS
    SELECT 1 as id, 'ORG1' as org_code, 'Organization One' as org_description
    UNION ALL
    SELECT 2, 'ORG2', 'Organization Two';
