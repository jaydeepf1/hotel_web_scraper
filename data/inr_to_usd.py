import math
import csv

exchange_rate = 0.01198


def get_usd_amount(inr_amount):
  inr_amount = int(inr_amount.replace(',', ''))
  amount_usd = inr_amount * exchange_rate
  return int(math.ceil(amount_usd))


def convert_inr_to_usd(file_name):
  with open(file_name, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)
    rows = list(reader)

  for row in rows:
    inr_amount = row[5]
    usd_amount = get_usd_amount(inr_amount)
    row[5] = str(usd_amount)

  with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)


convert_inr_to_usd(
    'raw/Louisville, KY, United States/Louisville_KY_United_States_07_03_2024_To_07_04_2024.csv'
)
convert_inr_to_usd(
    'raw/Louisville, KY, United States/Louisville_KY_United_States_07_04_2024_To_07_05_2024.csv'
)
convert_inr_to_usd(
    'raw/Louisville, KY, United States/Louisville_KY_United_States_07_05_2024_To_07_06_2024.csv'
)
