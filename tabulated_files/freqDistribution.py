#!/usr/bin/env python3

# Written by Hector Urbina
# <hurbinas@gmail.com>

import sys
import argparse

def main():

  commandLineParser = argparse.ArgumentParser(description="Prints frequency distribution table(s) for column(s) in input.")
  commandLineParser.add_argument(metavar='FILE', dest="inputFile", help='Tabulated input file with columns of numbers')
  commandLineParser.add_argument(metavar="INTERVALS", type=int, dest="nIntervals", help='Amount of intervals to split the data in')
  commandLineParser.add_argument('-c', '--column', type=int, dest="columns", nargs='+', default='1', help='columns to be considered, starting from 1. default: first column. To analyse all columns, use 0.')
  options = commandLineParser.parse_args()

  try:
    f = open(options.inputFile, "r")
  except IOError:
    print("Couldn't open " + options.inputFile)
    sys.exit()

  firstLoop = True
  hasHeaders = False
  data = []
  minData = []
  maxData = []
  for row in f:
    splittedRow = row.split("\t")
    if firstLoop:
      for n in splittedRow:
        data.append([])
        try:
          n = float(n)
        except:
          hasHeaders = True
        if type(n) != float:
          minData.append(float("inf"))
          maxData.append(float("-inf"))
        else:
          minData.append(n)
          maxData.append(n)
      firstLoop = False
    if hasHeaders:
      hasHeaders = False
      continue
    for i in range(len(splittedRow)):
      try:
        n = float(splittedRow[i])
      except:
        print("Error reading " + splittedRow[i] + " as a number, please fix and rerun", sys.stderr)
        sys.exit()
      data[i].append(n)
      if n < minData[i]:
        minData[i] = n
      if n > maxData[i]:
        maxData[i] = n
      
  classes = []
  for i in range(len(data)):
    r = maxData[i] - minData[i]
    classes.append([])
    l = r / options.nIntervals
    for cat in range(options.nIntervals):
      classes[i].append((minData[i] + cat * l, minData[i] + (1 + cat) * l))

  if type(options.columns) == int:
    options.columns = [options.columns]
  if 0 in options.columns:
    options.columns = range(len(data))
  else:
    for i in range(len(options.columns)):
      options.columns[i] -= 1

  for column in options.columns:
    d = data[column]
    counters = [0]*options.nIntervals
    for n in d:
      for c in range(options.nIntervals):
        (inferior,superior) = classes[column][c]
        if n <= superior:
          counters[c] += 1
          break
    print("distribution for column " + str(column + 1) + ":")
    for c in range(options.nIntervals):
      (inferior,superior) = classes[column][c]
      print("(" + str(inferior) + " - " + str(superior) + "]\t" + str(counters[c]))
    print()

main()
