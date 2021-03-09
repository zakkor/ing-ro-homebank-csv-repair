import csv

if __name__ == '__main__':
  txs = []
  with open('bank.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    tx = None
    for i, row in enumerate(reader):
      date = row[0]
      if date != '':
        if not date.split(' ')[0].isnumeric():
          # Ignore bogus lines
          continue
        if tx is not None:
          # Add previous transaction
          txs.append(tx)
        # Create new transaction
        tx = {'date': date, 'details': row[2], 'debit': row[5], 'credit': row[7]}
      elif tx is not None:
        # Append more details to the current transaction
        tx.update(details = tx['details']+';'+row[2])
  
  with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['date', 'details', 'debit', 'credit'])
    for tx in txs:
      writer.writerow(tx.values())