package com.example.secureapp;

import android.os.Bundle;
import android.view.WindowManager;
import android.widget.ListView;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;

public class ChatActivity extends AppCompatActivity {

    private ListView messageList;
    private EditText messageInput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        );
        setContentView(R.layout.activity_chat);

        messageList = findViewById(R.id.message_list);
        messageInput = findViewById(R.id.message_input);
        loadMessages();
    }

    private void loadMessages() {
        // Load chat messages
    }
}
