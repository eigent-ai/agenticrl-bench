package com.personnel;

import java.time.LocalDate;

public class BirthDateResolver {

    public static LocalDate resolveFromAge(int years, int months, int days, LocalDate referenceDate) {
        return referenceDate.minusDays(days).minusMonths(months).minusYears(years);
    }
}
