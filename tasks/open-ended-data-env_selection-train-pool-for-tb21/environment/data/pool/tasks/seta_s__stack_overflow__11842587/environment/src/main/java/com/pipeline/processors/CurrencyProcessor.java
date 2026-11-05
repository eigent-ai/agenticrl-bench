package com.pipeline.processors;

import org.apache.camel.Exchange;
import org.apache.camel.Processor;

import java.util.Map;

public class CurrencyProcessor implements Processor {

    @Override
    public void process(Exchange exchange) throws Exception {
        Boolean valid = exchange.getIn().getHeader("orderValid", Boolean.class);
        if (valid == null || !valid) return;

        @SuppressWarnings("unchecked")
        Map<String, String> order = (Map<String, String>) exchange.getIn().getBody();

        int quantity = Integer.parseInt(order.get("quantity"));
        double unitPrice = Double.parseDouble(order.get("unit_price"));
        String currency = order.get("currency");

        double revenue = quantity * unitPrice;

        if ("EUR".equalsIgnoreCase(currency)) {
            revenue = revenue * 0.85;
        }

        order.put("revenue", String.valueOf(revenue));
    }
}
