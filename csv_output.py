import csv


def write_to_csv(transactions):
    with open('transactions.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['Дата-времяТранзакции', 'Сумма', 'ТипТранзакции']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)
