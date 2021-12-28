package com.example.hornillapp_movil;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView hiperv =(TextView)findViewById(R.id.Hipervinculo);
        hiperv.setClickable(true);
        hiperv.setMovementMethod(LinkMovementMethod.getInstance());
        String text = "<a href='http://hornillapp.agrosavia.co:7000/'> Ir a Hornillapp WEB </a>";
        hiperv.setText(Html.fromHtml(text));
    }

    public void Ir_a_Form(View view) {
        startActivity(new Intent(MainActivity.this, Formulario.class));
    }
}