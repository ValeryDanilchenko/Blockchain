import hashlib
import json
import datetime
import random
import os


# Класс для добавления транзакций к блокам
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount
        }


# Класс создаюший блоки
class Block:
    def __init__(self, index, timestamp, transactions, previousHash="", nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()

    # Функция считающая хэш на основе данных в блоке
    def calculateHash(self):
        string = str(self.index) + self.previousHash + self.timestamp + \
                 json.dumps([tx.to_dict() for tx in self.transactions]) + str(self.nonce)
        return hashlib.sha256(string.encode()).hexdigest()

    # Майним
    def mineBlock(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculateHash()
        print("Block mined: " + self.hash)

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transaction': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previousHash,
            'hash': self.hash,
            'nonce': self.nonce
        }


# Класс создания цепочки
class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesis()]
        self.difficulty = 4
        self.pendingTransactions = []

    # Создаем начальный блок
    def createGenesis(self):
        return Block(0, "01/01/2018", [Transaction("Genesis", "Genesis", 0)], "0")

    # Формируем цепочку блоков
    def latestBlock(self):
        return self.chain[-1]

    # Добавляем транзакции в наш блок
    def addTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    # Генерируем хэш на основе списка транзакций
    def minePendingTransactions(self):
        block = Block(len(self.chain), datetime.datetime.now().strftime("%d/%m/%Y"), self.pendingTransactions,
                      self.latestBlock().hash, nonce=0)
        block.mineBlock(self.difficulty)
        self.chain.append(block)
        self.pendingTransactions = []

    # Проверка легитимности блоков
    def checkValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]
            if currentBlock.hash != currentBlock.calculateHash():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False
        return True


fakeUsers = ["Anna", "Ilya", "Kirill", "Ulyana", "Matvey",
             "Alice", "Denis", "Kira", "Konstantin", "Orel",
             "Nikita", "Krol", "Olga", "Prorok", "Ksenia",
             "Camilla", "Maksim", "Andrey", "Gregory", "Marina"]


def saveBlockchain(blockchain, path):
    blocks = []
    # Вывод цепочки в консоль
    for block in blockchain.chain:
        blocks.append(block.to_dict())
    with open(path, 'w') as outfile:
        json.dump(blocks, outfile, indent=4)


def start(num, path):
    testChain = Blockchain()
    try:
        os.remove(path)
    except OSError:
        pass
    # Имитация майнинга
    for i in range(1, num):
        print("Mining block...")
        for j in range(random.randint(1, 6)):
            testChain.addTransaction(Transaction(fakeUsers[random.randint(1, 19)], fakeUsers[random.randint(1, 19)],
                                                 random.randint(1, 100)))
        testChain.minePendingTransactions()
    print("Is blockchain valid?" + str(testChain.checkValid()))
    saveBlockchain(testChain, path)
    print(f"Blockchain is saved in {path}")


def main():
    try:
        num = int(input('Enter the desired number of blocks in the chain:'))
        path = input('Enter the file name under which the blockchain will be saved:')
        path = f'{path}.txt'
        start(num, path)
    except ValueError:
        print("Error! Enter an integer.")


if __name__ == '__main__':
    main()

