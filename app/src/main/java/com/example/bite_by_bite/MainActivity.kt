package com.example.bite_by_bite

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.bite_by_bite.ui.auth.SignInScreen
import com.example.bite_by_bite.ui.theme.Bite_By_BiteTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            Bite_By_BiteTheme {
                SignInScreen()
            }
        }
    }
}