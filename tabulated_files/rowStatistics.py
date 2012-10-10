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
  for row in fileReaders[0]:
    nums = []
    try:
      if options.columns == "all":
        nums = [float(n) for n in row]
      else:
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
          if options.columns == "all":
            nums.extend([float(n) for n in r])
          else:
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
    print("row " + str(rowNumber) + ": mean = " + str(mean) + ", std = " + str(std))
    rowNumber += 1

main()
