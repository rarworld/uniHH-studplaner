#! /usr/bin/env python3

from Parser import Parser
from Preparer import Preparer
from Merger import Merger
from Enricher import Enricher
import json

if __name__ == "__main__":
    with open("config.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    parser = Parser(jsonObject)
    parser.parsing()

    preparer = Preparer(jsonObject)
    preparer.preparing()

    merger = Merger(jsonObject)
    merger.merging()

    enricher = Enricher(jsonObject)
    enricher.enrich()