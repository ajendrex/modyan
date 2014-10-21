#!/usr/bin/env python3

# Written by Hector Urbina
# <hurbinas@gmail.com>

import sys
import argparse
import re
import pysam

def calcIdentityAndLengthFraction(r):
  seqLength = 0
  alignedLength = 0
  matches = 0
  for op,length in r.cigar:
    if op == 0:
      seqLength += length
      alignedLength += length
      matches += length
      continue
    if op == 1:
      seqLength += length
      alignedLength += length
      continue
    if op == 3:
      alignedLength += length
      continue
    if op == 4:
      seqLength += length
      continue
    if op == 5:
      seqLength += length
      continue
    if op == 7:
      seqLength += length
      alignedLength += length
      matches += length
      continue
    if op == 8:
      seqLength += length
      alignedLength += length
  return (matches / alignedLength, alignedLength / seqLength)

def main():

  commandLineParser = argparse.ArgumentParser(description="Filter a SAM file by alignment sequence identity and length fraction.")
  commandLineParser.add_argument(metavar='SAMFILE', dest="samfile", help='SAM input file.')
  commandLineParser.add_argument('-i', '--identity', dest="minIdentity", default=0, help='Sets the min identity. Default = 0.')
  commandLineParser.add_argument('-l', '--length-fraction', dest="minLengthFraction", default=0, help='Sets the min length fraction. Default = 0.')
  options = commandLineParser.parse_args()

  try:
    samfile = pysam.Samfile(options.samfile, "r")
  except Exception as e:
    print("No pudo leer el archivo %s: %s" % (options.samfile, e))
    sys.exit()

  print(samfile.text)
  for r in samfile:
    (identity, lengthFraction) = calcIdentityAndLengthFraction(r)
    if identity >= options.minIdentity and lengthFraction >= options.minLengthFraction:
      print(str(r))

main()
