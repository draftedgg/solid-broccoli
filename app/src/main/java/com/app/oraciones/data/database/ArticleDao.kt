package com.app.oraciones.data.database

import androidx.room.*
import com.app.oraciones.data.models.Article
import kotlinx.coroutines.flow.Flow

@Dao
interface ArticleDao {
    @Query("SELECT * FROM articles ORDER BY title")
    fun getAllArticles(): Flow<List<Article>>
    
    @Query("SELECT * FROM articles WHERE category = :category ORDER BY title")
    fun getArticlesByCategory(category: String): Flow<List<Article>>
    
    @Query("SELECT * FROM articles WHERE id = :id")
    suspend fun getArticleById(id: String): Article?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertArticles(articles: List<Article>)
    
    @Update
    suspend fun updateArticle(article: Article)
    
    @Query("DELETE FROM articles")
    suspend fun deleteAllArticles()
    
    @Query("SELECT COUNT(*) FROM articles")
    suspend fun getArticleCount(): Int
}
