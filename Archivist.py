#!/usr/bin/python3
# -*-coding: utf-8 -*

# import pickle


class Archivist:
    def __init__(self):
        self.file = None

    def open_file(self, filename):
        self.file = open(filename, 'w')

    def log(self, text: str):
        line = str(text) + '\n'
        self.file.write(line)

    def close(self):
        self.file.close()
