package com.personnel;

import java.time.LocalDate;

public class AgeCalculator {

    public static int calculateAge(LocalDate birthDate, LocalDate referenceDate) {
        return referenceDate.getYear() - birthDate.getYear();
    }

    public static int calculateAgeManual(int curMonth, int curDay, int curYear,
                                          int birthMonth, int birthDay, int birthYear) {
        int yearDif = curYear - birthYear;
        int age = 0;

        if (curMonth > birthMonth) {
            age = yearDif;
        } else if (curMonth < birthMonth) {
            age = yearDif - 1;
        } else {
            if (curDay > birthDay) {
                age = yearDif;
            } else if (curDay < birthDay) {
                age = yearDif - 1;
            }
        }
        return age;
    }
}
