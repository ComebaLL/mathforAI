# =================== Лаба3 =================== #

# =================== Задание 1 =================== #

x <- seq(-6, 6, length.out = 1000)
y <- sin(x)


windowsFonts(
		Segoe = windowsFont("Segoe UI"),
		Times = windowsFont("Times New Roman")
		)


par(bg = "#f0f0f0", mar = c(5,5,4,2))

dev.new()
# Создание слоя графики без осей
plot(x, y,
	type = "n", 		# не рисовать точки\линии
	axes = FALSE,		# отключение стандартных осей
	ann = FALSE,		# отключение стандартных подписей
	xlim = c(-6,6),
	ylim = c(-1.1, 1.1)
    )


# Рисуем оси, пересекающиеся в начале координат
abline( h = 0, col = "black", lwd = 1)
abline( v = 0, col = "black", lwd = 1)


# Рисуем сам график функций
lines(x, y, col = "darkblue", lwd = 3, lty = 1)


# Добавление подписей
axis(1, pos = 0, family = "Times", font = 2, cex.axis = 0.75, las = 1)
axis(2, pos = 0, family = "Times", font = 2, cex.axis = 0.75, las = 1)


# Названия
title(main = "График функции y = sin(x)",
	col.main = "black",
	family = "Segoe",
	font.main = 3
	)

# =================== Задание 2 =================== #

df <- read.csv2("данные.csv", fileEncoding = "cp1251")

df_clean <- na.omit(df[, c("Математика", "Обществознание")])

dev.new()
# Построение корреляционнго поля
plot(df_clean$Обществознание, df_clean$Математика,
	main = "Корреляционное поле и линии регрессии",
	xlab = "Баллы по обществознанию",
	ylab = "Баллы по математике",
	pch = 16,
	col = "gray70"
)


# Прямая регрессия
model1 <- lm(Математика ~ Обществознание, data = df_clean)
abline(model1, col = "red", lwd = 2)


# Обратная регрессия
model2 <- lm(Обществознание ~ Математика, data = df_clean)

cf <- coef(model2)
abline(a = -cf[1]/cf[2], b = 1/cf[2], col = "blue", lwd = 2, lty =2)


legend("topleft", legends = c("Мат ~ Общ пряма", "Общ ~ Мат обратная",
	col = c("red", "blue"),
	lwd = 2,
	lty = c(1,2)
)



# =================== Задание 3 =================== #

# Функция для отрисовки циферблата
draw_clock <- NA
draw_clock <- function() {
  # Настройка пустого холста
  plot(NULL, xlim = c(-1.2, 1.2), ylim = c(-1.2, 1.2), 
       asp = 1, axes = FALSE, ann = FALSE)
  
  # Рисуем внешний круг 
  symbols(0, 0, circles = 1, inches = FALSE, add = TRUE, lwd = 4, fg = "black")
  
  # Рисуем часовые деления
  angles <- seq(0, 2*pi, length.out = 13)[-13]
  # Длинные риски для часов
  segments(x0 = 0.9 * sin(angles), y0 = 0.9 * cos(angles),
           x1 = 1.0 * sin(angles), y1 = 1.0 * cos(angles), lwd = 3)
  
  # Рисуем цифры от 1 до 12
  hours <- 1:12
  h_angles <- pi/2 - (hours * (2*pi/12))
  
  text(x = 0.75 * cos(h_angles), 
       y = 0.75 * sin(h_angles), 
       labels = hours, 
       cex = 2, font = 2)
  
  # Рисуем стрелки (пусть будет 10:10)
  # Часовая стрелка
  arrows(0, 0, 0.4 * cos(pi/2 - 10.15 * (2*pi/12)), 
         0.4 * sin(pi/2 - 10.15 * (2*pi/12)), 
         lwd = 6, length = 0)
  
  # Минутная стрелка
  arrows(0, 0, 0.8 * cos(pi/2 - 10 * (2*pi/60)), 
         0.8 * sin(pi/2 - 10 * (2*pi/60)), 
         lwd = 4, length = 0)
  
  # Центральная точка
  points(0, 0, pch = 16, cex = 1.5)
}

# Сохранение в pdf
pdf("clock_face.pdf", width = 7, height = 7)
draw_clock()
dev.off()

# Сохранение в jpf
jpeg("clock_face.jpg", width = 800, height = 800, quality = 100, res = 100)
draw_clock()
dev.off()



# =================== Задание 4 =================== #

df <- read.csv2("данные.csv", fileEncoding = "cp1251")

df_clean <- na.omit(df[, c("Математика", "Обществознание", "Русский.язык")])


graphics.off()
windows(width = 7, height = 10)

par(mfrow = c(3,1), mar = c(4,4,3,2))

hist(df_clean$Математика,
     main = "Гистограмма по математике",
     xlab = "Баллы",
     ylab = "Частота",
     col = "skyblue",
     border = "white",
     family = "sans")

hist(df_clean$Русский.язык,
     main = "Гистограмма по русскому языку",
     xlab = "Баллы",
     ylab = "Частота",
     col = "skyblue",
     border = "white",
     family = "sans")

hist(df_clean$Обществознание,
     main = "Гистограмма по обществознанию",
     xlab = "Баллы",
     ylab = "Частота",
     col = "skyblue",
     border = "white",
     family = "sans")

par(mfrow = c(1,1))


# =================== Задание 5 =================== #

# Генерация данных (по 100 значений)
set.seed(123) 


# Равномерное на [0, 1]
data_unif <- runif(100, min = 0, max = 1)

# Нормальное (среднее будет 50, а стандартное отклонение 10)
data_norm <- rnorm(100, mean = 50, sd = 10)

# Хи-квадрат (5 степеней свободы)
data_chi  <- rchisq(100, df = 5)

# Функция для отрисовки пары (Гистограмма + Ящик)
draw_plots <- function(data, title_name) {
  # Делим окно на 2 части
  par(mfrow = c(2, 1), mar = c(4, 4, 3, 2))
  
  # Гистограмма
  hist(data, 
	 main = paste("Гистограмма:", title_name), 
       xlab = "Значения", 
	 ylab = "Частота", 
       col = "lightblue", 
	 border = "white", 	
	 family = "sans")
  
  # Ящик с усами (горизонтальный)
  boxplot(data, 
	    main = paste("Ящик с усами:", title_name), 
          horizontal = TRUE, 
	    col = "lightcoral", 
          xlab = "Значения", 	
	    family = "sans")
}

# Равномерное распределение 
windows(width = 8, height = 8)
draw_plots(data_unif, "Равномерное [0, 1]")

# Нормальное распределение 
windows(width = 8, height = 8)
draw_plots(data_norm, "Нормальное (m=50, sd=10)")

# ОКНО 3: Распределение Хи-квадрат 
windows(width = 8, height = 8)
draw_plots(data_chi, "Хи-квадрат (df=5)")

