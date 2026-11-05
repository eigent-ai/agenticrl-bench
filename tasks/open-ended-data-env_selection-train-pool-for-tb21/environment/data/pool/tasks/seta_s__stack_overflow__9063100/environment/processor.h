#ifndef PROCESSOR_H
#define PROCESSOR_H

typedef struct {
    char name[64];
    char card_number[20];
    double amount;
    char currency[4];
} Transaction;

int process_transactions(Transaction *txns, int count);
void mask_card(const char *card, char *masked, int len);

#endif
