import csv, sys

months_ro_en = {
  'ianuarie': 'january',
  'februarie': 'february',
  'martie': 'march',
  'aprilie': 'april',
  'mai': 'may',
  'iunie': 'june',
  'iulie': 'july',
  'august': 'august',
  'septembrie': 'september',
  'octombrie': 'october',
  'noiembrie': 'november',
  'decembrie': 'december',
}

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print('you must specify an input .csv file')
    exit(1)

  outfilename = sys.argv[2] if len(sys.argv) >= 3 else sys.argv[1].split('.csv')[0] + '_out.csv'
  txs = []
  with open(sys.argv[1], newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    tx = None
    for row in reader:
      date = row[0]
      if date != '':
        datewords = date.split(' ')
        if not datewords[0].isnumeric():
          # Ignore bogus lines
          continue
        if tx is not None:
          # Add previous transaction
          txs.append(tx)
        # Translate month name from RO to EN
        datewords[1] = months_ro_en[datewords[1]]
        # Create new transaction
        tx = {'date': ' '.join(datewords), 'details': row[2], 'debit': row[5], 'credit': row[7]}
      elif tx is not None:
        # Append more details to the current transaction
        tx.update(details = tx['details']+';'+row[2])
  
  with open(outfilename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['date', 'details', 'debit', 'credit'])
    for tx in txs:
      writer.writerow(tx.values())