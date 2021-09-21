from visualize import *

import math
import re

import bitstring
from bitstring import BitArray
class HuffmanTreeNode:

    def __init__(self, val, lch, rch):
        self.val = val
        self.lch = lch
        self.rch = rch

    def __str__(self):
        return "(HNode:" + str(self.val) + " " + str(self.lch) + " " + str(self.rch) + ")"

class HuffmanTree:

    root = None
    encode = {}

    def add(node0, node1):
        node = HuffmanTreeNode(node0[1]+node1[1], node0[0], node1[0])
        return node

    def preOrder(root, code):
        try:
            print(root)
            root.lch
            HuffmanTree.preOrder(root.lch, code + "0")
            HuffmanTree.preOrder(root.rch, code + "1")
        except:
            HuffmanTree.encode[root] = code


class TextProcessor:

    def __init__(self):
        self.text = ""
        self.frequencyDict = {}
        self.encoded = ""

    def read(self, text):
        self.text = text

    def charCounter(self):
        for c in self.text:
            if c not in self.frequencyDict:
                self.frequencyDict[c] = 0
            self.frequencyDict[c] += 1

    def treeBuilder(self):
        charEncounted = []
        buildTreeQueue = []
        _min = math.inf
        _mkey = ''
        for i in range(len(self.frequencyDict)):
            # find minimum frequency
            _min = math.inf
            for key in self.frequencyDict.keys():

                if key in charEncounted:
                    continue

                if _min > self.frequencyDict[key]:
                    _min = self.frequencyDict[key]
                    _mkey = key


            charEncounted.append(_mkey)
            buildTreeQueue.append([_mkey, _min])

        root = None
        while len(buildTreeQueue) != 1:
            buildTreeQueue.sort(key=lambda x: x[1], reverse=True)
            node0 = buildTreeQueue.pop()
            node1 = buildTreeQueue.pop()
            node = HuffmanTree.add(node0, node1)
            buildTreeQueue.append([node, node0[1]+node1[1]])

        HuffmanTree.root = buildTreeQueue[0][0]

        Structure(HuffmanTree.root).print()

        HuffmanTree.preOrder(HuffmanTree.root, "")


    def encoder(self):
        for c in self.text:
            self.encoded += HuffmanTree.encode[c]

        dict = ''.join(['{:b}'.format(ord(x.encode('utf-8'))) for x in str(self.frequencyDict)])
        encoded = dict + "0" * 32 + self.encoded
        return BitArray(bin=encoded)


    def fileDecoder(encoded):
        import json
        decode_text = ""
        buffer = ""
        header, encoded = encoded.bin.split("0"*32)
        print(header)
        print(encoded)
        print(BitArray(header))
        str_header = ''

        # for d in encoded:
        #     buffer += d
        #     for key in HuffmanTree.encode.keys():
        #         if HuffmanTree.encode[key] == buffer:
        #             decode_text += key
        #             buffer = ""
        #             break

        return decode_text


    def decoder(self):
        decode_text = ""
        buffer = ""
        for d in self.encoded:
            buffer += d
            for key in HuffmanTree.encode.keys():
                if HuffmanTree.encode[key] == buffer:
                    decode_text += key
                    buffer = ""
                    break

        return decode_text

    def log(self):
        print("Encode Dict:", HuffmanTree.encode)
        print("Text:", self.text)
        text_bin = bin(int.from_bytes(text.encode(), 'big'))
        print("    text-bin:", text_bin)
        print("    text-len:", len(text_bin))
        print("Encode:")
        print("    text-bin:", "0b" + self.encoded)
        print("    text-len:", len(self.encoded))
        print("Decode:")
        print("    call decoder():", self.decoder())


    def process(self, log=True):
        self.read(text)
        self.charCounter()
        self.treeBuilder()
        encoded_bytes = self.encoder()
        if log: self.log()
        return encoded_bytes


if __name__ == "__main__":
    text = "The quick brown fox jumped over the lazy dog"

    textProcessor = TextProcessor()
    textProcessor.process()



