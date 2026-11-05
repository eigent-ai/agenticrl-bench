CREATE TEMPORARY TABLE tmp_employees
  SELECT DISTINCT PersonId, Name, Job, Position FROM employees;

SELECT tmp_employees.PersonId,
       tmp_employees.Name,
       tmp_employees.Job,
       tmp_employees.Position,
       CL.Cost AS MajorCost,
       CL.Benefit AS MajorBenefit,
       Inter.Cost AS InternalCost,
       Inter.Benefit AS InternalBenefit
FROM tmp_employees
LEFT OUTER JOIN pricing AS CL ON CL.PersonId = tmp_employees.PersonId
    AND CL.PriceSchedule = 'Major-Client'
    AND CL.ExpireDate = '0000-00-00 00:00:00'
LEFT OUTER JOIN pricing AS Inter ON Inter.PersonId = tmp_employees.PersonId
    AND Inter.PriceSchedule = 'Internal-Client'
    AND Inter.ExpireDate = '0000-00-00 00:00:00';

DROP TEMPORARY TABLE tmp_employees;
