#!/usr/bin/env python2

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
    if op == 0 or op == 7: #MATCH and EQUAL
      seqLength += length
      alignedLength += length
      matches += length
      continue
    if op == 1 or op == 8: #INSERTION and MISMATCH
      seqLength += length
      alignedLength += length
      continue
    if op == 4 or op == 5: #SOFT_CLIP and HARD_CLIP
      seqLength += length
  try:
    return (matches / alignedLength, alignedLength / seqLength)
  except Exception:
    return (0,0)

def main():

  commandLineParser = argparse.ArgumentParser(description="Filter a SAM file by alignment sequence identity and length fraction.")
  commandLineParser.add_argument(metavar='SAMFILE', dest="samfile", help='SAM input file.')
  commandLineParser.add_argument('-i', '--identity', type=float, dest="minIdentity", default=0, help='Sets the min identity. Default = 0.')
  commandLineParser.add_argument('-l', '--length-fraction', type=float, dest="minLengthFraction", default=0, help='Sets the min length fraction. Default = 0.')
  options = commandLineParser.parse_args()

  try:
    samfile = pysam.Samfile(options.samfile, "r")
  except Exception as e:
    print("No pudo leer el archivo %s: %s" % (options.samfile, e))
    sys.exit()

  print(samfile.text)
  print >> sys.stderr, "minIdentity: " + str(options.minIdentity) + ", min length fraction: " + str(options.minLengthFraction)
  for r in samfile:
    (identity, lengthFraction) = calcIdentityAndLengthFraction(r)
    #print >> sys.stderr, "identity: " + str(identity) + ", length fraction: " + str(lengthFraction)
    if identity >= options.minIdentity and lengthFraction >= options.minLengthFraction:
      print(str(r))

main()
