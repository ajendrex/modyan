#!/usr/bin/env python3

# Written by Hector Urbina
# <hurbinas@gmail.com>

import sys
import argparse
import textwrap

def getNumber(s):
  try:
    return int(float(s))
  except:
    return False

def main():

  commandLineParser = argparse.ArgumentParser(description="Produces a nucleotid sequence from only SNPs positions")
  commandLineParser.add_argument(metavar='FILE', dest="inputFile", help='Tabulated input file with columns: Strain, Reference Position, Reference Base, Allele Base')
  commandLineParser.add_argument("-t", "--table", dest="tableMode", default=False, action="store_true", help="Prints a single file in table mode")
  options = commandLineParser.parse_args()

  try:
    f = open(options.inputFile, "r")
  except IOError:
    print("Couldn't open " + options.inputFile)
    sys.exit()

  SNPpositions = []
  reference = {}
  SNPs = {}
  strains = []
  for row in f:
    splittedRow = row.strip().split("\t")
    if len(splittedRow) < 4: continue
    position = getNumber(splittedRow[1])
    if (position):
      strain = splittedRow[0]
      if (strain not in strains):
        strains.append(strain)
      alleleNucleotid = splittedRow[3]
      if (position not in SNPpositions):
        SNPpositions.append(position)
        SNPs[position] = {}
        SNPs[position][strain] = alleleNucleotid
        reference[position] = splittedRow[2]
      else:
        SNPs[position][strain] = alleleNucleotid
        if (reference[position] != splittedRow[2]):
          print("Error!, reference sequence shows different nucleotids for the position " + str(position))
          sys.exit()

  SNPpositions.sort()
  strains.sort()
  if not options.tableMode:
    for strain in strains:
      seq = ""
      for position in SNPpositions:
        if (strain in SNPs[position]):
          seq += SNPs[position][strain]
        else:
          seq += reference[position]
      print(">" + strain)
      for line in textwrap.wrap(seq, width=80):
        print(line)
  else:
    print("position\t" + "\t".join(strains))
    for position in SNPpositions:
      print(position, end="")
      for strain in strains:
        if (strain in SNPs[position]):
          print("\t" + SNPs[position][strain], end="")
        else:
          print("\t" + reference[position], end="")
      print()


main()
