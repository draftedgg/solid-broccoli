package com.app.oraciones

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.lifecycle.lifecycleScope
import com.app.oraciones.data.DataManager
import com.app.oraciones.data.database.AppDatabase
import com.app.oraciones.data.repository.ArticleRepository
import com.app.oraciones.ui.screens.OracionesApp
import com.app.oraciones.ui.theme.OracionesTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    
    lateinit var repository: ArticleRepository
    lateinit var dataManager: DataManager
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Inicializar base de datos y repositorio
        val db = AppDatabase.getDatabase(applicationContext)
        repository = ArticleRepository(db.articleDao())
        dataManager = DataManager(applicationContext, repository)
        
        // Cargar datos desde assets a la BD (solo la primera vez)
        lifecycleScope.launch {
            dataManager.initializeDataIfEmpty()
        }
        
        setContent {
            OracionesTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    OracionesApp(repository = repository)
                }
            }
        }
    }
}
