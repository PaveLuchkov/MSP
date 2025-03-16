# import pandas as pd

# # Загрузка данных
# file_path = "MainDF.csv"  # Укажите путь к вашему CSV-файлу
# df = pd.read_csv(file_path)

# # Определяем индекс первого финансового показателя (после 'size_cat')
# start_col = df.columns.get_loc("size_cat") + 1

# # Выбираем только финансовые показатели
# financial_data = df.iloc[:, start_col:]

# # Группируем данные по компании и считаем пропуски
# missing_counts = financial_data.isnull().groupby(df['Компания']).sum()

# # Сортируем компании по общему числу пропусков в убывающем порядке
# missing_counts['Total Missing'] = missing_counts.sum(axis=1)
# missing_counts_sorted = missing_counts.sort_values(by='Total Missing', ascending=False)

# # Выводим топ-10 компаний с наибольшим числом пропусков
# print(missing_counts_sorted.head(250))





