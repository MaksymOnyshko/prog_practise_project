import csv


class Block:
    def __init__(self, block_id, view):
        self.block_id = block_id.strip().lower()  # Уніфікуємо ID
        self.view = int(view)


class Blockchain:
    def __init__(self):
        self.chain = []
        self.votes = set()

    def add_vote(self, block_id):
        self.votes.add(block_id.strip().lower())  # Уніфікуємо ID

    def add_block(self, block):
        if block.view == 0:  # Додаємо початковий блок
            self.chain.append(block)
            return

        if not self.chain:  # Якщо блокчейн порожній, а блок не має view=0 — відхиляємо
            return

        last_view = self.chain[-1].view

        if block.view == last_view + 1 and block.block_id in self.votes:
            self.chain.append(block)

    def build_from_csv(self, blocks_file, votes_file):
        # Завантажуємо голоси
        with open(votes_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    self.add_vote(row[0])

        # Завантажуємо блоки
        with open(blocks_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'id' in row and 'view' in row:  # PDF вказує, що id називається "id", а не "block_id"
                    block = Block(row['id'], row['view'])
                    self.add_block(block)

    def display_chain(self):
        if not self.chain:
            print("Ланцюг порожній або жоден блок не пройшов перевірку!")
            return
        print("Зібраний блокчейн:")
        for block in self.chain:
            print(f"Block ID: {block.block_id}, View: {block.view}")

    def save_to_csv(self, output_file):
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "view"])  # Відповідає формату з PDF
            for block in self.chain:
                writer.writerow([block.block_id, block.view])


# Запуск програми
blocks_file = "blocks.csv"
votes_file = "votes.csv"
output_file = "blocks_votes.csv"

blockchain = Blockchain()
blockchain.build_from_csv(blocks_file, votes_file)
blockchain.display_chain()
blockchain.save_to_csv(output_file)
