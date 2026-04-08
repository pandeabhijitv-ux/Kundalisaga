package com.kundalii.saga;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Simple text view for now
        TextView textView = new TextView(this);
        textView.setText("KundaliSaga\n\nPython integration ready.\nChaquopy is configured.");
        textView.setPadding(50, 50, 50, 50);
        textView.setTextSize(18);
        setContentView(textView);
    }
}
