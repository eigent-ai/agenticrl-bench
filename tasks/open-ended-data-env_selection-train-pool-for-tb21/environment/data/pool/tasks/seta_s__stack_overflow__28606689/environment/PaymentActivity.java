package com.example.secureapp;

import android.os.Bundle;
import android.view.WindowManager;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class PaymentActivity extends AppCompatActivity {

    private TextView amountField;
    private TextView cardNumberField;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_payment);

        amountField = findViewById(R.id.amount);
        cardNumberField = findViewById(R.id.card_number);
        loadPaymentDetails();
    }

    @Override
    protected void onResume() {
        super.onResume();
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        );
    }

    private void loadPaymentDetails() {
        // Load payment information from intent
    }
}
