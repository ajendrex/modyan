#!/usr/bin/env python3

# Written by Hector Urbina
# <hurbinas@gmail.com>

import sys
import argparse
import re
from Bio import SeqIO, SeqRecord, Seq

def main():

  commandLineParser = argparse.ArgumentParser(description="Prints useful information about sequences in multifasta.")
  commandLineParser.add_argument(metavar='fastaIN', dest="fasta", help='fasta input file.')
  commandLineParser.add_argument('-mm', '--minmax-length', dest="printMinMax", action='store_true', help='Prints the Min and Max sequence lengths.')
  commandLineParser.add_argument('-a', '--average-length', dest="printAverage", action='store_true', help='Prints the average sequence length.')
  commandLineParser.add_argument('-f', '--length-frequency', dest="printFreq", action='store_true', help='Prints a list of lengths with their frequency.')
  options = commandLineParser.parse_args()

  maxLength = 0
  minLength = float('inf')
  lengths = {}
  lengthsSum = 0
  nSeqs = 0

  inputHandle = open(options.fasta, "rU")
  for record in SeqIO.parse(inputHandle, "fasta"):
    nSeqs += 1
    if (options.printMinMax or options.printAverage or options.printFreq):
      l = len(record)
      if l > maxLength:
        maxLength = l
      if l < minLength:
        minLength = l
      if l in lengths:
        lengths[l] += 1
      else:
        lengths[l] = 1
      lengthsSum += l
  
  inputHandle.close()

  print("This fasta has " + str(nSeqs) + " sequences.")
  if (options.printMinMax):
    print("min sequence length: " + str(minLength))
    print("max sequence length: " + str(maxLength))
  if (options.printAverage):
    print("Average sequence length: " + str(lengthsSum * 1.0 / nSeqs))
  if (options.printFreq):
    print("Length\tSeqs")
    for l in sorted(lengths.keys()):
      print(str(l) + "\t" + str(lengths[l]))

main()
