package com.app.oraciones.data.models

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "articles")
data class Article(
    @PrimaryKey
    val id: String,
    val title: String,
    val content: String,
    val category: String,
    val url: String,
    val isFavorite: Boolean = false
)
