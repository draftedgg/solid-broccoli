package com.app.oraciones.data.repository

import com.app.oraciones.data.database.ArticleDao
import com.app.oraciones.data.models.Article
import kotlinx.coroutines.flow.Flow

class ArticleRepository(private val articleDao: ArticleDao) {
    val allArticles: Flow<List<Article>> = articleDao.getAllArticles()
    
    fun getArticlesByCategory(category: String): Flow<List<Article>> =
        articleDao.getArticlesByCategory(category)
    
    suspend fun getArticleById(id: String): Article? =
        articleDao.getArticleById(id)
    
    suspend fun insertArticles(articles: List<Article>) =
        articleDao.insertArticles(articles)
    
    suspend fun updateArticle(article: Article) =
        articleDao.updateArticle(article)
    
    suspend fun deleteAllArticles() =
        articleDao.deleteAllArticles()
    
    suspend fun getArticleCount(): Int =
        articleDao.getArticleCount()
    
    suspend fun toggleFavorite(article: Article) {
        articleDao.updateArticle(article.copy(isFavorite = !article.isFavorite))
    }
}
