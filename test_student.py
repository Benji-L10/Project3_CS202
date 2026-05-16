import unittest
from proj3 import (
    Node,
    MinHeap,
    heapify_up,
    heapify_down,
    insert,
    extract_min,
    count_frequency,
    create_priority_queue,
    build_tree_from_queue,
    generate_codes,
    encode,
    decode,
    huffman_encoding,
)


class TestHeapFunctions(unittest.TestCase):
    def test_heapify_up(self) -> None:
        heap = MinHeap([
            Node(3, "a"),
            Node(8, "b"),
            Node(5, "c"),
            Node(12, "d"),
            Node(10, "e"),
            Node(7, "f"),
            Node(2, "g"),
        ])
        result = heapify_up(heap, 6)
        self.assertEqual([n.freq for n in result.data], [2, 8, 3, 12, 10, 7, 5])

    def test_insert(self) -> None:
        heap = MinHeap([Node(5, "a"), Node(8, "b"), Node(7, "c")])
        result = insert(heap, Node(3, "d"))
        self.assertEqual(result.data[0], Node(3, "d"))
        self.assertEqual(len(result.data), 4)

    def test_extract_min(self) -> None:
        heap = MinHeap([Node(1, "a"), Node(3, "b"), Node(8, "c"), Node(5, "d")])
        new_heap, min_node = extract_min(heap)
        self.assertEqual(min_node, Node(1, "a"))
        self.assertEqual([n.freq for n in new_heap.data], [3, 5, 8])

    def test_heapify_down(self) -> None:
        heap = MinHeap([Node(9, "a"), Node(3, "b"), Node(5, "c")])
        result = heapify_down(heap, 0)
        self.assertEqual([n.freq for n in result.data], [3, 9, 5])


class TestHuffmanWorkflow(unittest.TestCase):
    def test_count_frequency(self) -> None:
        self.assertEqual(count_frequency("aaabbc"), {"a": 3, "b": 2, "c": 1})

    def test_create_priority_queue(self) -> None:
        pq = create_priority_queue({"a": 3, "b": 2, "c": 1})
        self.assertEqual(len(pq.data), 3)
        self.assertEqual(pq.data[0], Node(1, "c"))

    def test_generate_codes_single_char(self) -> None:
        root = Node(4, "a")
        codes = generate_codes(root)
        self.assertEqual(codes, {"a": "0"})

    def test_encode_decode_single_char(self) -> None:
        encoded, decoded, codes = huffman_encoding("aaaa")
        self.assertEqual(decoded, "aaaa")
        self.assertEqual(codes, {"a": "0"})
        self.assertEqual(encoded, "0000")

    def test_encode_decode_repeated(self) -> None:
        encoded, decoded, codes = huffman_encoding("aaabbc")
        self.assertEqual(decoded, "aaabbc")
        self.assertEqual(set(codes.keys()), {"a", "b", "c"})

    def test_hello(self) -> None:
        encoded, decoded, codes = huffman_encoding("hello")
        self.assertEqual(encoded, "1111100010")
        self.assertEqual(decoded, "hello")
        self.assertEqual(codes, {"l": "0", "o": "10", "e": "110", "h": "111"})


if __name__ == "__main__":
    unittest.main()