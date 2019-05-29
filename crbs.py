#!/bin/bash

import json
from pprint import pprint
import traceback
import shutil


class Bookmarks():

    def __init__(self, filepath):
        with open(filepath, "r") as fp:
            self.core = json.load(fp)

    @property
    def bar(self):
        return self.core['roots']['bookmark_bar']


class Node():

    def __init__(self, core):
        super(Node, self).__init__()
        self.core = core

    @property
    def children(self):
        if self.core.get('children'):
            return self.core['children']
        return list()

    @property
    def url(self):
        if self.core.get('url'):
            return self.core['url']
        return "Folder"
    
    @property
    def id(self):
        return self.core['id']

    @property
    def name(self):
        return self.core['name']

    @property
    def type(self):
        return self.core['type']

    def __repr__(self):
        return "{} ({})".format(
            self.name,
            self.url
        )


def recurse(n, indent):
    for n_ in sorted(n.children, key=lambda a: a['url']):
        node = Node(n_)
        i = 0
        for r in roots:
            print(i, r['name'])
            i += 1

        print(node, "in", n.name)

        try:
            new_dir = input("> ")
            if new_dir:
                roots[int(new_dir)]['children'].append(n_)
                n.children.remove(n_)
        except Exception as e:
            traceback.print_exc()

        recurse(node, indent + 1)


shutil.copy("Bookmarks", "Bookmarks.bak")
        
try:
    root = Bookmarks("Bookmarks")
    bookmarks = Node(root.bar)

    roots = sorted(bookmarks.children, key=lambda a: a['name'])

    (unsorted,) = [n for n in root.core['roots']['bookmark_bar']['children'] if n['name'].lower() == "unsorted"]

    try:
        recurse(Node(unsorted), 0)
    except KeyboardInterrupt:
        pass

    print("Saving")

    with open("Bookmarks", "w") as fp:
        json.dump(root.core, fp, indent=2)
finally:
    pass
