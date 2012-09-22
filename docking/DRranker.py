#!/usr/bin/python

import sys
import argparse
from csv import DictReader
import copy

def basename(filename):
  return filename[:filename.rfind(".")]

def insertLineToRanking(element,ranking):
  (line,avgScore) = element
  i = 0
  for i in range(0,len(ranking)):
    (oLine, oAvgScore) = ranking[i]
    if oAvgScore > avgScore:
      break
    if i == len(ranking) - 1:
      i += 1
  ranking.insert(i,element)

def rankByPresence(data):
  ranking = {}
  smile2rank = {}

  for i in range(1,len(data) + 1):
    ranking[i] = {}

  i = 0
  for fileContent in data:
    for lig in fileContent:
      fileContent[lig]["file"] = i
      if lig in smile2rank:
        r = smile2rank[lig]
        ranking[r+1][lig] = copy.deepcopy(ranking[r][lig])
        ranking[r+1][lig].append(fileContent[lig])
        del ranking[r][lig]
        smile2rank[lig] = r+1
      else:
        smile2rank[lig] = 1
        ranking[1][lig] = copy.deepcopy([fileContent[lig]])
    i += 1

  return ranking

def readInputFile(f):
  try:
    DR = open(f, "r")
  except IOError:
    print("Couldn't open " + f)
  reader = DictReader(DR, delimiter='\t')

  fileContent = {}
  
  for row in reader:
    key = row["Smiles"]
    if key in fileContent:
      if float(row["Total Score"]) > fileContent[key]["Score"]:
        continue
    else:
      fileContent[key] = {}

    fileContent[key]["Score"] = float(row["Total Score"])
    fileContent[key]["Name"] = row["Name"]

  DR.close()

  return fileContent

def first(o):
  (f,s) = o
  return f

def main():

  commandLineParser = argparse.ArgumentParser(description="Docking Results ranker: order docking results according to the presence of ligands and their average energy")
  commandLineParser.add_argument('files', metavar='DR', nargs='+', help='Docking Results file')
  options = commandLineParser.parse_args()

  data = []

  for inputFile in options.files:
    data.append(readInputFile(inputFile))

  ranking = rankByPresence(data)

  print("Smiles", end="")
  for f in options.files:
    print("\t" + basename(f),end="")
  print("\taverage Score")

  for r in range(len(options.files),0,-1):
    print("RANKING " + str(r) + ":")
    thisRanking = []
    for lig in ranking[r]:
      line = lig
      j = 0
      sumScore = 0
      for d in ranking[r][lig]:
        i = d["file"]
        for k in range(j,i):
          line += "\t-,-"
        j = i + 1
        score = d["Score"]
        sumScore += score
        line += "\t(" + d["Name"] + "," + str(score) + ")"
      for k in range(j,len(options.files)):
        line += "\t-,-"
      avgScore = sumScore / len(ranking[r][lig])
      line += "\t" + str(avgScore)
      insertLineToRanking((line,avgScore),thisRanking)
    print("\n".join(map(first,thisRanking)))

main()
