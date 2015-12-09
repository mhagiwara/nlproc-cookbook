import sys
import xml.etree.ElementTree as ET


def iterate_sentence(document_root):
    """Given the root node of XML Element Tree, iterates over all sentence text.

    Parameters:
        document_root: XML Element pointing to the root 'document' node

    Returns:
        iterator over sentence (string)
    """
    for sentence_node in document_root:
        words = []
        for word_node in sentence_node:
            if word_node.tag == 'w':
                words.append(word_node.text)
        yield ' '.join(words)


def main():
    tree = ET.parse(sys.argv[1])
    document_root = tree.getroot()

    for sentence in iterate_sentence(document_root):
        print sentence


if __name__ == '__main__':
    main()
