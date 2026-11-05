package com.pipeline.processors;

import org.apache.camel.Exchange;
import org.apache.camel.Processor;

import java.util.Map;

public class CategoryProcessor implements Processor {

    @Override
    public void process(Exchange exchange) throws Exception {
        Boolean valid = exchange.getIn().getHeader("orderValid", Boolean.class);
        if (valid == null || !valid) return;

        @SuppressWarnings("unchecked")
        Map<String, String> order = (Map<String, String>) exchange.getIn().getBody();

        String category = order.get("category");
        if (category != null) {
            order.put("category", category.toLowerCase().trim());
        }
    }
}
