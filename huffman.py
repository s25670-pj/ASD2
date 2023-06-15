import heapq # Importuje moduł do manipulacji kolejką priorytetową reprezentowaną przez kopiec typu min

class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency  # Definiuje operator mniejszości (<) dla węzłów Huffmana

def build_frequency_table(text):
    """
    Tworzy tablicę częstości dla podanego tekstu.
    """
    frequency_table = {}
    for char in text:
        if char in frequency_table:
            frequency_table[char] += 1
        else:
            frequency_table[char] = 1
    return frequency_table

def build_huffman_tree(frequency_table):
    """
    Buduje drzewo Huffmana na podstawie tablicy częstości.
    """
    priority_queue = []
    for char, frequency in frequency_table.items():
        heapq.heappush(priority_queue, HuffmanNode(char, frequency))

    while len(priority_queue) > 1:
        node1 = heapq.heappop(priority_queue)
        node2 = heapq.heappop(priority_queue)
        merged_frequency = node1.frequency + node2.frequency
        merged_node = HuffmanNode(None, merged_frequency)
        merged_node.left = node1
        merged_node.right = node2
        heapq.heappush(priority_queue, merged_node)

    return heapq.heappop(priority_queue)

def build_encoding_table(huffman_tree):
    """
    Buduje tablicę kodowania na podstawie drzewa Huffmana.
    """
    encoding_table = {}
    build_encoding_table_recursive(huffman_tree, "", encoding_table)
    return encoding_table

def build_encoding_table_recursive(node, code, encoding_table):
    """
    Rekurencyjnie buduje tablicę kodowania na podstawie drzewa Huffmana.
    """
    if node.char is not None:
        encoding_table[node.char] = code
    else:
        build_encoding_table_recursive(node.left, code + "0", encoding_table)
        build_encoding_table_recursive(node.right, code + "1", encoding_table)


def compress_text(text, encoding_table):
    """
    Kompresuje tekst na podstawie tablicy kodowania.
    """
    compressed_text = ""
    for char in text:
        compressed_text += encoding_table[char]
    return compressed_text

def write_compressed_file(compressed_text, encoding_table, output_file):
    """
    Zapisuje skompresowany tekst do pliku wyjściowego wraz z jawnie podanym słownikiem kodów.
    """
    with open(output_file, "wb") as file:
        # Zapisz słownik kodów jako nagłówek
        header = ""
        for char, code in encoding_table.items():
            header += char + code
        header_length = len(header)
        file.write(header_length.to_bytes(2, byteorder="big"))  # Zapisz długość nagłówka jako 2-bajtowa wartość
        file.write(header.encode("utf-8"))

        # Zapisz skompresowany tekst jako dane binarne
        compressed_bytes = int(compressed_text, 2).to_bytes((len(compressed_text) + 7) // 8, byteorder="big")
        file.write(compressed_bytes)

def compress_file(input_file, output_file):
    """
    Kompresuje plik na podstawie podanego pliku wejściowego i zapisuje skompresowane dane do pliku wyjściowego.
    """
    with open(input_file, "r") as file:
        text = file.read().rstrip()

    frequency_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(frequency_table)
    encoding_table = build_encoding_table(huffman_tree)
    compressed_text = compress_text(text, encoding_table)

    write_compressed_file(compressed_text, encoding_table, output_file)
