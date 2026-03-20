# ================== Лаба 5 ================== #


library(readxl)


file_path <- "ks.xlsx"

sheets <- excel_sheets(file_path)


alter <- c("two.sided", "greater", "less")


par(mfrow = c(1, length(sheets)))


for (i in 1:length(sheets)) {
  
	df <- read_excel(file_path, sheet = i)
  
	x <- na.omit(as.numeric(df[[1]]))
	y <- na.omit(as.numeric(df[[2]]))
  
  	# Проведение тестов Колмогорова-Смирнова
  	for (alt in alternatives) {

      	res <- ks.test(x, y, alternative = alt)

   		cat(sprintf("Альтернатива: %-10s | D-статистика: %.4f | p-value: %.4f\n", 
                alt, res$statistic, res$p.value))
  	}
  
	e1 <- ecdf(x)
	e2 <- ecdf(y)
  
  # Рисуем первый график
	plot(e1, 
		main = paste("ECDF для листа:", sheets[i]),
	      col = "blue", 
      	verticals = TRUE, 
	      do.points = FALSE,
	      xlab = "Значения",
	      ylab = "Fn(x)",
	      xlim = range(c(x, y))) 
  
  # Накладываем второй график
	lines(e2, 
	      col = "red", 
		verticals = TRUE, 
	      do.points = FALSE)
  
  # Добавляем легенду
	legend("bottomright", 
		legend = c("Выборка X", "Выборка Y"), 
		col = c("blue", "red"), 
		lty = 1)
}

par(mfrow = c(1,1))