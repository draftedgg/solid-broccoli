package com.app.oraciones.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.app.oraciones.data.models.Article
import com.app.oraciones.data.repository.ArticleRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ArticleViewModel(
    private val repository: ArticleRepository,
    private val articleId: String
) : ViewModel() {
    private val _article = MutableStateFlow<Article?>(null)
    val article: StateFlow<Article?> = _article.asStateFlow()
    
    init {
        viewModelScope.launch {
            _article.value = repository.getArticleById(articleId)
        }
    }
    
    fun toggleFavorite() {
        viewModelScope.launch {
            _article.value?.let { art ->
                repository.toggleFavorite(art)
                _article.value = art.copy(isFavorite = !art.isFavorite)
            }
        }
    }
    
    class Factory(
        private val repository: ArticleRepository,
        private val articleId: String
    ) : ViewModelProvider.Factory {
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            if (modelClass.isAssignableFrom(ArticleViewModel::class.java)) {
                @Suppress("UNCHECKED_CAST")
                return ArticleViewModel(repository, articleId) as T
            }
            throw IllegalArgumentException("Unknown ViewModel class")
        }
    }
}
