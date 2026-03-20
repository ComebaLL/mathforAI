# ================ Лаба 6 ================ #


# ================ Задание 1 ================ #


data <- read.csv2("связи.csv")


cor_matrix <- cor(data, use = "complete.obs", method = "pearson")
cat("Матрица корреляции\n")
print(round(cor_matrix,4))

# Получаем названия столбцов
cols <- colnames(data)

# Проходим циклом по всем уникальным парам
for (i in 1:(length(cols) - 1)) {
  for (j in (i + 1):length(cols)) {
    
    col1 <- cols[i]
    col2 <- cols[j]
    
    # Выполняем тест на значимость
    test_res <- cor.test(data[[col1]], data[[col2]], method = "pearson")
    
    cat("Коэффициент r:", round(test_res$estimate, 4), "\n")
  }
}


# ================ Задание 2 ================ #


linmod <- lm(y ~ x, data= df)

cat("Суммарная информация")
print(summary(linmod))

cat("Кол-во обхектов внутри")
n_elemets <- length(linmod)
cat("Кол-во обхектов внутри\n", n_elemets, "\n")
cat("название элементов модели\n")
print(names(linmod))


plot(df$x, df$y,
	main = "Линейная регрессия y на x",
	xlab = "Вектор X",
	ylab = "Вектор Y",
	pch = 19, col = "blue")

abline(linmod, col = "red", lwd = 2)


