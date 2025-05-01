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


class BSTNode:
    def __init__(self, block):
        self.block = block
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, block):
        if self.root is None:
            self.root = BSTNode(block)
        else:
            self._insert(self.root, block)

    def _insert(self, node, block):
        if block.view < node.block.view:
            if node.left is None:
                node.left = BSTNode(block)
            else:
                self._insert(node.left, block)
        else:
            if node.right is None:
                node.right = BSTNode(block)
            else:
                self._insert(node.right, block)

    def pre_order(self, node):
        if node:
            print(node.block.view, end=' ')
            self.pre_order(node.left)
            self.pre_order(node.right)

    def in_order(self, node):
        if node:
            self.in_order(node.left)
            print(node.block.view, end=' ')
            self.in_order(node.right)

    def post_order(self, node):
        if node:
            self.post_order(node.left)
            self.post_order(node.right)
            print(node.block.view, end=' ')

    def is_full(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return True
        if not node.left and not node.right:
            return True
        if node.left and node.right:
            return self.is_full(node.left) and self.is_full(node.right)
        return False

    def is_complete(self):
        if not self.root:
            return True

        queue = [self.root]
        encountered_none = False

        while queue:
            current = queue.pop(0)
            if current:
                if encountered_none:
                    return False
                queue.append(current.left)
                queue.append(current.right)
            else:
                encountered_none = True
        return True

    def is_perfect(self):
        def depth(node):
            d = 0
            while node:
                d += 1
                node = node.left
            return d

        def is_perfect_rec(node, d, level=0):
            if not node:
                return True
            if not node.left and not node.right:
                return d == level + 1
            if not node.left or not node.right:
                return False
            return (is_perfect_rec(node.left, d, level + 1) and
                    is_perfect_rec(node.right, d, level + 1))

        d = depth(self.root)
        return is_perfect_rec(self.root, d)


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


class TreeAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.blocks = []
        self.bst = BinarySearchTree()

    def load_blocks(self):
        with open(self.filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'id' in row and 'view' in row:
                    block = Block(row['id'], row['view'])
                    self.blocks.append(block)

    def build_tree(self):
        for block in self.blocks:
            self.bst.insert(block)

    def analyze(self):
        print("\n--- Аналіз дерева з blocks_votes.csv ---")
        print("\nPre-order traversal:")
        self.bst.pre_order(self.bst.root)
        print("\nIn-order traversal:")
        self.bst.in_order(self.bst.root)
        print("\nPost-order traversal:")
        self.bst.post_order(self.bst.root)

        print("\n\nTree type:")
        print("Full:", self.bst.is_full())
        print("Complete:", self.bst.is_complete())
        print("Perfect:", self.bst.is_perfect())



blocks_file = "blocks.csv"
votes_file = "votes.csv"
output_file = "blocks_votes.csv"

votes = Votes()
votes.load_from_csv(votes_file)

blockchain = Chain(votes)
blockchain.build_from_csv(blocks_file)
blockchain.display_chain()
blockchain.save_to_csv(output_file)

analyzer = TreeAnalyzer(output_file)
analyzer.load_blocks()
analyzer.build_tree()
analyzer.analyze()
