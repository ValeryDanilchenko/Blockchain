import json
import os

def checkBlock(path):
    with open(path, 'r') as file:
        data = json.load(file)

    for block_data in data:
        print('Block index:', block_data['index'])
        print('Timestamp:', block_data['timestamp'])
        print('Transactions:')
        for tx in block_data['transaction']:
            print('  ', tx['sender'], '->', tx['receiver'], '(', tx['amount'], ')')
        print('Previous hash:', block_data['previous_hash'])
        print('Hash:', block_data['hash'])
        print('Nonce:', block_data['nonce'])
        print()


def main():
    path = input('Enter path to thread you want to read: ')
    if os.path.isfile(path):
        try:
            checkBlock(path)
        except ValueError:
            print('Error! Invalid data in file.')
    else:
        print('Error! File not found at the specified path.')


if __name__ == '__main__':
    main()