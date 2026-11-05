package com.invoices;

import java.util.Date;
import java.util.concurrent.TimeUnit;

public class LateFeeService {

    private static final double DAILY_FEE = 5.0;

    public double assessLateFee(int invoiceId, Date referenceDate) {
        Date now = new Date();
        long diffMillis = now.getTime() - referenceDate.getTime();
        long daysLate = TimeUnit.DAYS.convert(diffMillis, TimeUnit.MILLISECONDS);

        if (daysLate <= 0) {
            return 0.0;
        }
        return daysLate * DAILY_FEE;
    }
}
