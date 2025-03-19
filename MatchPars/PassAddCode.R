pass52 <- read.csv("companies_data_52.csv", stringsAsFactors = FALSE, header = FALSE)
colnames(pass52) <- c("Компания", "Город", "Продукт", "Технология", "Год")
head(pass52)


# Объединяем, выбирая только нужные столбцы из pass52
okved52 <- okved52 %>%
  left_join(pass52 %>%
              select(Компания, Год, Продукт, Технология), 
            by = c("Компания" = "Компания", "year" = "Год"))

write.csv(okved52, "okved52.csv", row.names = FALSE)
write.csv(pass52, "pass52.csv", row.names = FALSE)