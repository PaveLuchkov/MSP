library(dplyr)
my_data <- readRDS("high_tech.rds")
process_file <- function(file_path, industry_name) {
  companies_data <- read.csv(file_path, stringsAsFactors = FALSE)
  my_data <- readRDS("high_tech.rds")
  city_data <- read.csv("city.csv")
  normalize <- function(x) {
    x <- tolower(x)
    x <- trimws(x)
    return(x)
  }
  normalize_string <- function(x) {
    x <- tolower(x)
    x <- gsub("\\s*\\(.*?\\)", "", x)
    x <- gsub("\\b(ооо|оао|зao|ип|нко|фгуп|акционерное общество|публичное акционерное общество|закрытое акционерное общество|группа компаний|торговый дом|сеть универсамов|компания|корпорация|ранее)\\b", "", x)
    x <- gsub(",.*", "", x)
    x <- gsub("\\b(филиал|цех)\\s*№?\\d*\\b", "", x)
    x <- gsub("\\b\\d+\\b", "", x)
    x <- gsub("[-:]", " ", x)
    x <- gsub("[\"'`,]", "", x)
    x <- gsub("[[:punct:]]", "", x)
    x <- gsub("\\s+", " ", x)
    x <- trimws(x)
    return(x)
  }
  
  companies_data$normalized_city <- normalize(companies_data$Город)
  city_data$normalized_city <- normalize(city_data$city)
  city_data$normalized_region <- normalize(city_data$region)
  my_data$normalized_region <- normalize(my_data$region)
  companies_data$normalized_name <- normalize_string(companies_data$Компания)
  my_data$normalized_name <- normalize_string(my_data$name)
  
  companies_data <- companies_data %>% 
    left_join(city_data[, c("normalized_city", "normalized_region")], 
              by = c("normalized_city" = "normalized_city"))
  companies_data$Регион <- ifelse(is.na(companies_data$normalized_region), companies_data$normalized_city, companies_data$normalized_region)
  companies_data <- companies_data %>% 
    select(-normalized_region)
  
  companies_data$region <- sub("^([^ ]+).*", "\\1", companies_data$Регион)
  companies_data <- companies_data %>% 
    select(-Регион)
  
  matched_data <- merge(companies_data, my_data, 
                        by.x = c("normalized_name"), 
                        by.y = c("normalized_name"), 
                        all.x = TRUE, all.y = FALSE)
  
  matched_data <- matched_data %>% 
    filter(!is.na(size_cat) & size_cat != "" & size_cat != " " & size_cat != 0)
  matched_data$normalized_region <- sub("^([^ ]+).*", "\\1", matched_data$normalized_region)
  
  matched_data <- matched_data %>% 
    filter(region.x == normalized_region)
  matched_data <- matched_data %>% 
    group_by(Компания) %>% 
    filter(n_distinct(firm_inn) == 1) %>% 
    ungroup()
  
  matched_data <- matched_data %>% 
    select(-normalized_city, -region.x, -normalized_region, -normalized_name, -head_name,-head_job, -phone, -email, -site)
  
  quantitative_columns <- c("income", "expenses", "intangibles", "fixed_assets", 
                            "noncurrent_assets", "inventory", "net_assets", 
                            "receivables", "current_assets", "assets", 
                            "lt_debt", "st_debt", "passive", 
                            "nwc", "equity", "total_debt", "sales", "cgs", 
                            "commercial", "admin_expenses", "interest_paid", 
                            "ebt", "eat", "ebit", "labor_costs", "interest_payment")
  
  matched_data <- matched_data %>% 
    mutate(across(all_of(quantitative_columns), 
                  ~ ifelse(year == 2023, as.numeric(.) / 1000, as.numeric(.))))
                  
  write.csv(matched_data, paste0("matched_results/matched_", industry_name, ".csv"), row.names = FALSE)
  okved <- matched_data
  
  unique_companies <- okved %>% 
    select(Компания) %>% 
    distinct()
  write.csv(unique_companies, paste0("matched_results/unique_", industry_name, ".csv"), row.names = FALSE)
}

files <- list.files("industries_df", full.names = TRUE, pattern = "\\.csv$")

for (file in files) {
  industry_name <- tools::file_path_sans_ext(basename(file))
  process_file(file, industry_name)
}
