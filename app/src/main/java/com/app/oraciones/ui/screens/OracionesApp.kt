package com.app.oraciones.ui.screens

import androidx.compose.runtime.Composable
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument

@Composable
fun OracionesApp() {
    val navController = rememberNavController()
    
    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(
                onCategoryClick = { categoryId ->
                    navController.navigate("category/$categoryId")
                }
            )
        }
        
        composable(
            route = "category/{categoryId}",
            arguments = listOf(navArgument("categoryId") { type = NavType.StringType })
        ) { backStackEntry ->
            val categoryId = backStackEntry.arguments?.getString("categoryId") ?: ""
            val categoryName = when(categoryId) {
                "oraciones" -> "Oraciones"
                "devociones" -> "Devociones"
                "novenas" -> "Novenas"
                "rosarios" -> "Rosarios"
                "mensajes" -> "Mensajes"
                "biblioteca" -> "Biblioteca"
                "otros" -> "Otros"
                else -> "Categoría"
            }
            
            CategoryScreen(
                categoryId = categoryId,
                categoryName = categoryName,
                onArticleClick = { articleId ->
                    navController.navigate("article/$articleId")
                },
                onBackClick = { navController.popBackStack() }
            )
        }
        
        composable(
            route = "article/{articleId}",
            arguments = listOf(navArgument("articleId") { type = NavType.StringType })
        ) { backStackEntry ->
            val articleId = backStackEntry.arguments?.getString("articleId") ?: ""
            
            ArticleScreen(
                articleId = articleId,
                onBackClick = { navController.popBackStack() }
            )
        }
    }
}
