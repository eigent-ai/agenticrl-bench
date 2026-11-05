package com.pipeline.processors;

import org.apache.camel.Exchange;
import org.apache.camel.Processor;
import com.pipeline.SummaryData;

import java.util.Map;

public class AggregationProcessor implements Processor {

    @Override
    public void process(Exchange exchange) throws Exception {
        @SuppressWarnings("unchecked")
        Map<String, String> order = (Map<String, String>) exchange.getIn().getBody();
        Boolean valid = exchange.getIn().getHeader("orderValid", Boolean.class);

        SummaryData summary = new SummaryData();

        if (valid != null && valid) {
            String category = order.get("category");
            double revenue = Double.parseDouble(order.get("revenue"));
            summary.addValidOrder(category, revenue);
        } else {
            String fileName = order.get("_file");
            int lineNum = Integer.parseInt(order.getOrDefault("_line", "0"));
            String reason = order.getOrDefault("_reason", "unknown");
            summary.addInvalidOrder(fileName, lineNum, reason);
        }
    }
}
