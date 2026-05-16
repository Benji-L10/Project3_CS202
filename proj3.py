from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: Node | None = None
    right: Node | None = None

    def __str__(self) -> str:
        return f"Node: {self.char}, Freq: {self.freq}"


@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)


def _swap(data: list[Node], i: int, j: int) -> list[Node]:
    new_data = data[:]
    new_data[i], new_data[j] = new_data[j], new_data[i]
    return new_data


def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    if index <= 0:
        return heap

    parent = (index - 1) // 2
    if heap.data[index] < heap.data[parent]:
        return heapify_up(MinHeap(_swap(heap.data, index, parent)), parent)

    return heap


def insert(heap: MinHeap, element: Node) -> MinHeap:
    new_data = heap.data + [element]
    return heapify_up(MinHeap(new_data), len(new_data) - 1)


def heapify_down(heap: MinHeap, index: int) -> MinHeap:
    size = len(heap.data)
    left = 2 * index + 1
    right = 2 * index + 2

    if left >= size:
        return heap

    smallest = left
    if right < size and heap.data[right] < heap.data[left]:
        smallest = right

    if heap.data[smallest] < heap.data[index]:
        return heapify_down(MinHeap(_swap(heap.data, index, smallest)), smallest)

    return heap


def extract_min(heap: MinHeap) -> tuple[MinHeap, Node]:
    if len(heap.data) == 0:
        raise IndexError("Cannot extract from an empty heap")

    if len(heap.data) == 1:
        return MinHeap([]), heap.data[0]

    min_node = heap.data[0]
    last = heap.data[-1]
    new_data = [last] + heap.data[1:-1]
    return heapify_down(MinHeap(new_data), 0), min_node


def count_frequency(s: str) -> dict[str, int]:
    freq: dict[str, int] = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def create_priority_queue(frequency: dict[str, int]) -> MinHeap:
    heap = MinHeap([])
    for ch, count in frequency.items():
        heap = insert(heap, Node(count, ch))
    return heap


def build_tree_from_queue(priority_queue: MinHeap) -> Node:
    if len(priority_queue.data) == 0:
        raise ValueError("Cannot build tree from empty priority queue")

    if len(priority_queue.data) == 1:
        return priority_queue.data[0]

    heap1, node1 = extract_min(priority_queue)
    heap2, node2 = extract_min(heap1)

    merged = Node(
        node1.freq + node2.freq,
        min(node1.char, node2.char),
        node1,
        node2
    )

    heap3 = insert(heap2, merged)
    return build_tree_from_queue(heap3)


def build_tree(priority_queue: MinHeap) -> Node:
    return build_tree_from_queue(priority_queue)


def generate_codes(
    node: Node | None,
    prefix: str = "",
    code: dict | None = None
) -> dict:
    if code is None:
        code = {}

    if node is None:
        return code

    if node.left is None and node.right is None:
        if prefix == "":
            return {**code, node.char: "0"}
        return {**code, node.char: prefix}

    left_codes = generate_codes(node.left, prefix + "0", code)
    return generate_codes(node.right, prefix + "1", left_codes)


def encode(s: str, codes: dict) -> str:
    return "".join(codes[ch] for ch in s)


def decode(encoded_string: str, root: Node) -> str:
    if encoded_string == "":
        return ""

    if root.left is None and root.right is None:
        return root.char * len(encoded_string)

    result: list[str] = []
    current = root

    for bit in encoded_string:
        if bit == "0":
            if current.left is None:
                raise ValueError("Invalid encoded string")
            current = current.left
        elif bit == "1":
            if current.right is None:
                raise ValueError("Invalid encoded string")
            current = current.right
        else:
            raise ValueError("Encoded string must contain only 0 and 1")

        if current.left is None and current.right is None:
            result.append(current.char)
            current = root

    return "".join(result)


def huffman_encoding(s: str):
    # Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)
    root = build_tree_from_queue(pq)
    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string, root)
    return encoded_string, decoded_string, codes