#!/usr/bin/env python3

# Written by Hector Urbina
# <hurbinas@gmail.com>

import sys
import argparse
import csv
import numpy

def main():

  commandLineParser = argparse.ArgumentParser(description="Prints row statistics from a (set of) tabulated input file(s)")
  commandLineParser.add_argument(metavar='FILE', nargs='+', dest="inputFiles", help='Tabulated input files with numbers in columns to be considered (See -c flag)')
  commandLineParser.add_argument('-c', '--column', dest="columns", nargs='+', default='all', help='columns to be considered, starting from 1. default: all columns.')
  commandLineParser.add_argument('-d', '--detailed', dest="detailed", default=False, action='store_true', help='Prints columns before statistics.')
  options = commandLineParser.parse_args()

  files = []
  fileReaders = []

  for filename in options.inputFiles:
    try:
      files.append(open(filename, "r"))
    except IOError:
      print("Couldn't open " + filename)
      sys.exit()

  for f in files:
    fileReaders.append(csv.reader(f, delimiter='\t'))

  rowNumber = 1
  printHeaders = True
  for row in fileReaders[0]:
    nums = []
    try:
      if options.columns == "all":
        options.columns = [x+1 for x in range(len(row))]
      for column in options.columns:
        nums.append(float(row[int(column)-1]))
    except ValueError:
      rowNumber += 1
      if len(fileReaders) > 1:
        for reader in fileReaders[1:]:
          next(reader)
      continue
    except IndexError:
      print("Your column indexes are out of bounds")
      sys.exit()

    try:
      if len(fileReaders) > 1:
        for reader in fileReaders[1:]:
          r = next(reader)
          for column in options.columns:
            nums.append(float(r[int(column)-1]))
    except ValueError:
      print("One of the files (not the first one given) has a non-numeric value where the first one does have it. Line " + str(rowNumber))
      sys.exit()
    except IndexError:
      print("Your column indexes are out of bounds")
      sys.exit()

    npNums = numpy.array(nums)
    mean = npNums.mean()
    std = npNums.std()
    if printHeaders:
      columnNames = ["row"]
      if options.detailed:
        for f in options.inputFiles:
          columnNames.extend(["col" + str(c) + "_" + f for c in options.columns])
      columnNames.extend(["mean", "std"])
      print("\t".join(columnNames))
      printHeaders = False

    print(str(rowNumber) + "\t", end="")
    if options.detailed:
      print("\t".join([str(n) for n in nums]), end="")
      print("\t", end="")
    print(str(mean) + "\t" + str(std))
    rowNumber += 1

main()
