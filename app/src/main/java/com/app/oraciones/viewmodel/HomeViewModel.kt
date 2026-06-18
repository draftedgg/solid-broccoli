package com.app.oraciones.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.app.oraciones.data.models.Category
import com.app.oraciones.data.repository.ArticleRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class HomeViewModel(private val repository: ArticleRepository) : ViewModel() {
    private val _articleCount = MutableStateFlow(0)
    val articleCount: StateFlow<Int> = _articleCount.asStateFlow()
    
    val categories = listOf(
        Category("oraciones", "Oraciones", "🙏"),
        Category("devociones", "Devociones", "✝️"),
        Category("novenas", "Novenas", "9️⃣"),
        Category("rosarios", "Rosarios", "📿"),
        Category("mensajes", "Mensajes", "📜"),
        Category("biblioteca", "Biblioteca", "📚"),
        Category("otros", "Otros", "⭐")
    )
    
    init {
        viewModelScope.launch {
            _articleCount.value = repository.getArticleCount()
        }
    }
    
    class Factory(private val repository: ArticleRepository) : ViewModelProvider.Factory {
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            if (modelClass.isAssignableFrom(HomeViewModel::class.java)) {
                @Suppress("UNCHECKED_CAST")
                return HomeViewModel(repository) as T
            }
            throw IllegalArgumentException("Unknown ViewModel class")
        }
    }
}
