package com.app.oraciones.data

import android.content.Context
import com.app.oraciones.data.models.Article
import com.app.oraciones.data.repository.ArticleRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray

class DataManager(
    private val context: Context,
    private val repository: ArticleRepository
) {
    suspend fun initializeDataIfEmpty() {
        if (repository.getArticleCount() > 0) return
        
        withContext(Dispatchers.IO) {
            try {
                val jsonStr = context.assets.open("oraciones.json")
                    .bufferedReader()
                    .use { it.readText() }
                
                val jsonArray = JSONArray(jsonStr)
                val articles = mutableListOf<Article>()
                
                for (i in 0 until jsonArray.length()) {
                    val obj = jsonArray.getJSONObject(i)
                    articles.add(
                        Article(
                            id = obj.getString("id"),
                            title = obj.getString("title"),
                            content = obj.getString("content"),
                            category = obj.getString("category"),
                            url = obj.getString("url"),
                            isFavorite = false
                        )
                    )
                }
                
                repository.insertArticles(articles)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
