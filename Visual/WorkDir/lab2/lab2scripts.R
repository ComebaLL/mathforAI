# ======================== 2ая лаба ======================== #

df <- read.csv2("данные.csv", fileEncoding = "cp1251")

print(df)

# ======================== Задание 2 ======================== #

df_clean <- na.omit(df)

# ======================== Задание 3 ======================== #

df_sorted <- df_clean[order(df_clean$Пол, -df_clean$Математика),]

print(df_sorted)

# ======================== Задание 4 ======================== #

table(df_clean$Пол)

# ======================== Задание 5 ======================== #

df_math <- df_clean$Математика

print(df_math)

# Среднее выборочное 
m_mean <- mean(df_math)
print(m_mean)


# Выборочная дисперсия
m_var <- var(df_math)
print(m_var)


# Среднеквадратичное отклонение
m_sd <- sd(df_math)
print(m_sd)

# Квартели
m_qurtly <- quantile(df_math)
print(m_qurtly)


# Гистограмма
hist(df_math)


# ======================== Задание 6 ======================== #

n <- length(df_math)

k <- 1 + floor(log2(n))

# Границы
v_min <- min(df_math)
v_max <- max(df_math)

step <- (v_max - v_min) / k

# Вектор границ
breaks <- seq(v_min, v_max, length.out = k + 1)

freq_vector <- numeric(k)

# Цикл для подсчета частот

for (i in 1:k) {
	lower <- breaks[i]
	upper <- breaks[i+1]
	
	if (i < k) {
		count <- sum(df_math >= lower & df_math < upper)
	}
	else {
		count <- sum(df_math >= lower & df_math <= upper)
	}
	
	freq_vector[i] <- count
}

print(freq_vector)

