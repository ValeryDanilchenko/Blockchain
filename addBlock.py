import blockchain
from blockchain import Blockchain, Block, Transaction
import json
import os


def readBlockchain(path):
    with open(path, 'r') as f:
        data = json.load(f)

    curblockchain = Blockchain()
    for block_data in data:
        block = Block(
            block_data['index'],
            block_data['timestamp'],
            [Transaction(tx['sender'], tx['receiver'], tx['amount']) for tx in block_data['transaction']],
            block_data['previous_hash'],
            block_data['nonce']
        )
        curblockchain.chain.append(block)

    addNewTran(curblockchain, path)


def addNewTran(curblockchain, path):
    while True:
        response = input('Do you want to add a block to the chain? (yes/no) ')
        if response.lower() == 'yes':
            transactions = []
            while True:
                sender, receiver, amount = input('Enter sender, receiver, and amount (e.g. sender receiver 100): ').split()
                amount = int(amount)
                transactions.append(Transaction(sender, receiver, amount))
                response = input('Do you want to add another transaction to this block? (yes/no) ')
                if response.lower() == 'no':
                    break
            for t in range(len(transactions)):
                curblockchain.addTransaction(transactions[t])
            curblockchain.minePendingTransactions()
            print('Block added to chain.')
            blockchain.saveBlockchain(curblockchain, path)
        elif response.lower() == 'no':
            break
        else:
            print('Invalid response. Please enter "yes" or "no".')


def main():
    path = input('Enter path to chain you want to add block: ')
    if os.path.isfile(path):
        try:
            readBlockchain(path)
        except ValueError:
            print('Error! Invalid data in file.')
    else:
        print('Error! File not found at the specified path.')


if __name__ == '__main__':
    main()
