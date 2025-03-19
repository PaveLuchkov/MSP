library(dplyr)

# Получаем список файлов в папке matched_results, которые начинаются с unique
unique_files <- list.files("matched_results", full.names = TRUE, pattern = "^unique_.*\\.csv$")

# Инициализируем пустой data frame для объединения всех компаний
all_unique_companies <- data.frame(Компания = character())

# Обрабатываем каждый файл
for (file in unique_files) {
  # Читаем данные из файла
  unique_companies <- read.csv(file)
  
  # Приводим столбец Компания к типу character
  unique_companies$Компания <- as.character(unique_companies$Компания)
  
  # Объединяем данные
  all_unique_companies <- bind_rows(all_unique_companies, unique_companies)
}

# Убираем дубликаты
all_unique_companies <- all_unique_companies %>% distinct()

# Сохраняем объединенный список уникальных компаний
write.csv(all_unique_companies, "matched_results/all_unique_companies.csv", row.names = FALSE)