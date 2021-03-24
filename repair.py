#!/usr/bin/env python3

import csv, sys

months_ro_en = {
  'ianuarie': '01',
  'februarie': '02',
  'martie': '03',
  'aprilie': '04',
  'mai': '05',
  'iunie': '06',
  'iulie': '07',
  'august': '08',
  'septembrie': '09',
  'octombrie': '10',
  'noiembrie': '11',
  'decembrie': '12',
}

column_positions = {
  's': {
    'date': 0,
    'details': 2,
    'debit': 5,
    'credit': 7,
  },
  't': {
    'date': 0,
    'details': 3,
    'debit': 4,
    'credit': 6,
  },
}

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print('you must specify a mode: `-t` for transactions or `-s` for statement, and an input .csv file')
    exit(1)

  mode = sys.argv[1][1]
  if mode != 't' and mode != 's':
    print(mode)
    print('you must specify a mode: `-t` for transactions or `-s` for statement')
    exit(1)
  cols = column_positions[mode]
  outfilename = sys.argv[3] if len(sys.argv) >= 4 else sys.argv[2].split('.csv')[0] + '_out.csv'
  txs = []
  with open(sys.argv[2], newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    tx = None
    for row in reader:
      date = row[cols['date']]
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
        tx = {
          'date': '-'.join(datewords),
          'details': row[cols['details']],
          'debit': row[cols['debit']],
          'credit': row[cols['credit']],
        }
      elif tx is not None:
        # Append more details to the current transaction
        tx.update(details = tx['details']+';'+row[cols['details']])
    # Add final transaction
    txs.append(tx)
  
  with open(outfilename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(['date', 'details', 'debit', 'credit'])
    for tx in txs:
      writer.writerow(tx.values())