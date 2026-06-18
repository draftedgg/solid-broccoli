package com.app.oraciones.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF6B4423),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFD4A574),
    secondary = Color(0xFF8B6F47),
    background = Color(0xFFF5F5DC),
    surface = Color.White
)

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFFD4A574),
    onPrimary = Color(0xFF3E2723),
    primaryContainer = Color(0xFF6B4423),
    secondary = Color(0xFFBCAAA4),
    background = Color(0xFF1C1B1F),
    surface = Color(0xFF2D2A2E)
)

@Composable
fun OracionesTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography(),
        content = content
    )
}
