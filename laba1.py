import csv


class Block:
    def __init__(self, block_id, view):
        self.block_id = block_id.strip().lower()
        self.view = int(view)


class Votes:
    def __init__(self):
        self.votes = set()

    def add_vote(self, block_id):
        self.votes.add(block_id.strip().lower())

    def has_vote(self, block_id):
        return block_id.strip().lower() in self.votes

    def load_from_csv(self, votes_file):
        with open(votes_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    self.add_vote(row[0])


class Chain:
    def __init__(self, votes):
        self.chain = []
        self.votes = votes

    def add_block(self, block):
        if block.view == 0:
            self.chain.append(block)
            return

        if not self.chain:
            return

        last_view = self.chain[-1].view

        if block.view == last_view + 1 and self.votes.has_vote(block.block_id):
            self.chain.append(block)

    def build_from_csv(self, blocks_file):
        with open(blocks_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'id' in row and 'view' in row:
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
            writer.writerow(["id", "view"])
            for block in self.chain:
                writer.writerow([block.block_id, block.view])



blocks_file = "blocks.csv"
votes_file = "votes.csv"
output_file = "blocks_votes.csv"

votes = Votes()
votes.load_from_csv(votes_file)

blockchain = Chain(votes)
blockchain.build_from_csv(blocks_file)
blockchain.display_chain()
blockchain.save_to_csv(output_file)
