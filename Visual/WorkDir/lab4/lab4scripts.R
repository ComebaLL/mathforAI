# ===================== Лаба 4 ===================== #

# ===================== Задание 1 ===================== #

install.packages("readxl")

library(readxl)

data <- read_excel("данные.xlsx", sheet= "Стьюдент1")

x_values <- na.omit(data$X)

mu_check <- c(8,6)

alternatives <- c("two.sided", "greater", "less")

for (mu0 in mu_check) {
	cat("Проверка нулевой гипотезы H0: mu =", mu0, "\n")
  
  	for (alt in alternatives) {
    	# Выполняем t-тест
    	res <- t.test(x_values, mu = mu0, alternative = alt)
    
    	# Формируем текст альтернативной гипотезы для вывода
    	alt_text <- switch(alt,
                       "two.sided" = "mu != ",
                       "greater"   = "mu >  ",
                       "less"      = "mu <  ")
    
    	cat(sprintf("H1: %s %d | p-value = %.4f | ", alt_text, mu0, res$p.value))
    
    	# Интерпретация результата (уровень значимости 0.05)
    	if (res$p.value < 0.05) {
      	cat("Результат: H0 отвергается\n")
    	} else {
      	cat("Результат: H0 не отвергается\n")
    	}
  	}
}


# ===================== Задание 2 ===================== #

df <- read_excel("данные.xlsx", sheet= "Стьюдент4")


x <- na.omit(as.numeric(df$X))
y <- na.omit(as.numeric(df$Y))

alter <- c("two.sided", "greater", "less")

cat("Проверка гипотезы H0 mu_x = mu_y")


for (alt in alter){
	res <- t.test(x,y, alter = alt, var.equal = TRUE)
	
	alt_desc <- switch(alt,
				"two.sided" = "H1 mu_x != mu_y",
				"greater" = "H1 mu_x > mu_y",
				"less" = "H1 mu_x < mu_y")
	cat("\nАльтернативная гипотеза:", alt_desc, "\n")
	cat("t-статистика:",round(res$statistic,4), "\n")
	cat("p-value:", format.pval(res$p.value,digits=4), "\n")

	if (res$p.value < 0.05){
		cat("Результат H0 отклоняется")
	} else {
		cat("Результат H0 не отклоняется")
	}
}



# ===================== Задание 3 ===================== #

df <- read_excel("данные.xlsx", sheet= "Стьюдент3")


x <- na.omit(as.numeric(df$X))
y <- na.omit(as.numeric(df$Y))

alter <- c("two.sided", "greater", "less")

cat("Проверка гипотезы H0 mu_x = mu_y")

for (alt in alter){
	res <- t.test(x,y, alter = alt, var.equal = FALSE)
	
	alt_desc <- switch(alt,
				"two.sided" = "H1 mu_x != mu_y",
				"greater" = "H1 mu_x > mu_y",
				"less" = "H1 mu_x < mu_y")
	cat("\nАльтернативная гипотеза:", alt_desc, "\n")
	cat("t-статистика:",round(res$statistic,4), "\n")
	cat("p-value:", format.pval(res$p.value,digits=4), "\n")
	cat("Степени свободы:", round(res$parameter, 2), "\n")

	if (res$p.value < 0.05){
		cat("Результат H0 отклоняется")
	} else {
		cat("Результат H0 не отклоняется")
	}
}
