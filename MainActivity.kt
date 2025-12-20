package com.example.project

// Импорт необходимых библиотек для Android, Compose и корутин
import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.res.colorResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.project.ui.theme.ProjectTheme
import androidx.compose.material3.Icon
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.foundation.border
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.Color
import kotlinx.coroutines.delay
import kotlin.random.Random

// Главный класс активности приложения
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Установка содержимого экрана через Compose
        setContent {
            MyScreenPreview()
        }
    }
}

@Composable
private fun MyScreen(){
    // --- Инициализация состояний (State) ---
    // remember позволяет сохранить значение переменной при перерисовке (recomposition)
    // mutableStateOf делает переменную "наблюдаемой" — когда она меняется, экран обновляется
    
    var default by remember { mutableStateOf(2) } // Базовое значение клика
    var w by remember { mutableStateOf(2.dp) }   // Ширина границы для кнопки Auto
    var ww by remember { mutableStateOf(2.dp) }  // Ширина границы для кнопки Ratio
    var nclick by remember { mutableStateOf(true) } // Флаг: можно ли еще нажать на Ratio
    var pressed by remember { mutableStateOf(false) } // Состояние кнопки Auto (нажата/нет)
    
    // rememberSaveable сохраняет данные даже при повороте экрана
    var ratio by rememberSaveable { mutableIntStateOf(2) } // Текущий множитель клика
    var clicks by rememberSaveable { mutableIntStateOf(0) } // Общий счетчик кликов
    
    // Лямбда-функция для добавления очков
    val addClick: (Int) -> Unit = { x -> clicks = clicks + x }
    
    var boostTime by rememberSaveable { mutableIntStateOf(0) } // Таймер усиления x2
    var autoTime by rememberSaveable { mutableIntStateOf(0) }  // Состояние автокликера

    // --- Побочные эффекты (Side Effects) ---
    
    // LaunchedEffect для таймера буста. Запускается при изменении boostTime
    LaunchedEffect(boostTime) {
        if (boostTime > 0) {
            delay(1000) // Задержка 1 секунда
            boostTime-- // Уменьшение времени

            if (boostTime == 0) {
                ratio = default // Возврат к обычному значению после окончания буста
            }
        }
    }

    // LaunchedEffect для автокликера. Работает в цикле, пока autoTime > 0
    LaunchedEffect(autoTime) {
        while (autoTime > 0) {
            delay(1000) // Ждем секунду
            addClick(ratio) // Автоматически добавляем текущий ratio к счету
        }
    }

    // --- Верстка интерфейса ---
    // Box — контейнер, позволяющий накладывать элементы друг на друга или выравнивать их
    Box(modifier = Modifier
        .fillMaxSize()
        .padding(horizontal = 50.dp, vertical = 30.dp)
    ){
        // Центральная кнопка (Нос собаки) для кликов
        Box(modifier = Modifier
            .width(60.dp)
            .align(Alignment.Center)
            .aspectRatio(1f)
            .background(color = colorResource(R.color.white))
            .clickable { addClick(ratio) } // При клике вызываем функцию добавления
        ){
            Icon(
                painter = painterResource(R.drawable.dognose),
                contentDescription = null
            )
        }

        // Кнопка усиления "x2" (Буст)
        Box(modifier = Modifier
            .width(100.dp)
            .align(Alignment.BottomCenter)
            .aspectRatio(1f)
            .border(2.dp, Color.Black)
            .clickable {
                clicks = clicks - 50 // Списание стоимости (50 кликов)
                ratio = default * 2  // Удвоение множителя
                boostTime = 10       // Установка таймера на 10 секунд
            }
        ){
            Text(
                text = "  x2",
                fontSize = 50.sp,
                modifier = Modifier.align(Alignment.CenterStart)
            )
        }

        // Кнопка "Ratio" — установка случайного базового значения
        Box(modifier = Modifier
            .width(100.dp)
            .align(Alignment.BottomStart)
            .aspectRatio(1f)
            .border(ww, Color.Black)
            .clickable {
                if (nclick) { // Сработает только один раз
                    default = Random.nextInt(1, 10) // Случайное число от 1 до 9
                    ratio = default
                    nclick = false
                    ww = 5.dp // Визуальное изменение границы после активации
                }
            }
        ){
            Text(
                text = "Ratio",
                fontSize = 30.sp,
                modifier = Modifier.align(Alignment.Center)
            )
        }

        // Кнопка "Auto" — включение/выключение автокликера
        Box(modifier = Modifier
            .width(100.dp)
            .align(Alignment.BottomEnd)
            .border(w, Color.Black)
            .aspectRatio(1f)
            .clickable {
                if(pressed){
                    ratio = default
                    w = 2.dp
                    pressed = false
                    autoTime = 0 // Выключение
                } else {
                    ratio = 1 // При автоклике множитель сбрасывается в 1 (логика автора)
                    w = 5.dp
                    pressed = true
                    autoTime = 1 // Включение
                }
            }
        ){
            Text(
                text = "  Auto",
                fontSize = 30.sp,
                modifier = Modifier.align(Alignment.CenterStart)
            )
        }

        // Отображение текущего счета
        Text(
            text = clicks.toString(),
            fontSize = 30.sp,
            modifier = Modifier.align(Alignment.TopEnd)
        )

        // Логика выбора картинки собаки (зависит от активного буста x2)
        val dogPainter = if (ratio == default * 2)
            painterResource(R.drawable.angrydog)
        else
            painterResource(R.drawable.dog)

        // Отображение иконки собаки с использованием смещения (offset)
        Icon(
            painter = dogPainter,
            contentDescription = null,
            modifier = Modifier
                .size(300.dp)
                .offset(x = 0.dp, y = 200.dp)
        )
    }
}

// Функция для предварительного просмотра в среде разработки
@Preview(showBackground = true)
@Composable
fun MyScreenPreview() {
    MyScreen()
}