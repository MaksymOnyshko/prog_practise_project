import csv


class Block:
    def __init__(self, block_id, view):
        self.block_id = block_id
        self.view = int(view)


class Blockchain:
    def __init__(self):
        self.chain = []
        self.votes = set()

    def add_vote(self, block_id):
        self.votes.add(block_id)

    def add_block(self, block):
        if block.view == 0 or (self.chain and block.view - 1 == self.chain[-1].view and block.block_id in self.votes):
            self.chain.append(block)

    def build_from_csv(self, blocks_file, votes_file):
        with open(votes_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    self.add_vote(row[0])

        with open(blocks_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'block_id' in row and 'view' in row:
                    block = Block(row['block_id'], row['view'])
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
            writer.writerow(["block_id", "view"])
            for block in self.chain:
                writer.writerow([block.block_id, block.view])


blocks_file = "blocks.csv"
votes_file = "votes.csv"
output_file = "blocks_votes.csv"

blockchain = Blockchain()
blockchain.build_from_csv(blocks_file, votes_file)
blockchain.display_chain()
blockchain.save_to_csv(output_file)