#!/usr/bin/env python3

# Written by Hector Urbina
# <hurbinas@gmail.com>

import sys
import argparse
import re
from Bio import SeqIO, SeqRecord, Seq

def main():

  commandLineParser = argparse.ArgumentParser(description="Split squences from fasta according to a given separator.")
  commandLineParser.add_argument(metavar='fastaIN', dest="fasta", help='fasta input file.')
  commandLineParser.add_argument(metavar='fastaOUT', dest="out", help='fasta output file name.')
  commandLineParser.add_argument('-s', '--separator', dest="sep", default='n', help='Separator to be used.')
  options = commandLineParser.parse_args()

  inputHandle = open(options.fasta, "rU")
  outputHandle = open(options.out, "w")
  for record in SeqIO.parse(inputHandle, "fasta"):
    i = 1
    seqName = record.id
    for subseq in re.split(options.sep + '+', str(record.seq)):
      myRecord = SeqRecord.SeqRecord(Seq.Seq(subseq))
      myRecord.id = seqName + "_part" + str(i)
      myRecord.description = ""
      SeqIO.write(myRecord, outputHandle, "fasta")
      sys.stdout.flush()
  
  inputHandle.close()
  outputHandle.close()

main()
