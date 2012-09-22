#!/usr/bin/env python3

# Written by Hector Urbina
# <hurbinas@gmail.com>

import sys
import argparse
from csv import DictReader

def checkForPermeations(initials,permeating,atomCoords,frame,prevFrame,minCoord,maxCoord,minDist):
  toDel = []
  for atomIndex in permeating.keys():
    if atomIndex not in atomCoords[frame]:
      (frame1,coord1) = permeating[atomIndex]
      frame2 = prevFrame
      coord2 = atomCoords[prevFrame][atomIndex]
      if maxCoord - coord1 < minDist and coord2 - minCoord < minDist or coord1 - minCoord < minDist and maxCoord - coord2 < minDist:
        print("\t".join(map(str,[atomIndex,prevFrame,coord1,frame,coord2])))
      #else:
        #print("discarded: " + str(coord1) + " -> " + str(coord2) + " at frames " + str(frame1) + " and " + str(frame2))
      toDel.append(atomIndex)
  for atomIndex in toDel:    
    del permeating[atomIndex]

  toDel = []
  for atomIndex in initials:
    if atomIndex not in atomCoords[frame]:
      toDel.append(atomIndex)
  for atomIndex in toDel:
    del initials[atomIndex]
  
  for atomIndex in atomCoords[frame]:
    if atomIndex not in permeating:
      if atomIndex not in initials:
        permeating[atomIndex] = (frame,atomCoords[frame][atomIndex])
  
  if prevFrame in atomCoords:
    del atomCoords[prevFrame]

def main():

  commandLineParser = argparse.ArgumentParser(description="Prints permeation events of atoms through a coordinate in a trajectory")
  commandLineParser.add_argument('atomInfoFile', help='Atoms info file. Tab Separated Values: frame index x y z')
  commandLineParser.add_argument('-a', '--axis', dest="axis", choices='xyz', default='z', help='Axis where permeation events are being monitored. Default: z')
  commandLineParser.add_argument('minCoord', type=float, help='lowest coordinate for a permeation event to occur')
  commandLineParser.add_argument('maxCoord', type=float, help='highest coordinate for a permeation event to occur')
  commandLineParser.add_argument('-d', '--axis_distance', dest="minDist", type=float, default=2.0, help='min distance (angstroms) from max or min coordinate to consider a valid permeation event. Default = 2')
  options = commandLineParser.parse_args()

  try:
    f = open(options.atomInfoFile, "r")
  except IOError:
    print("Couldn't open " + atomInfoFile)
  reader = DictReader(f, delimiter='\t')

  if options.minCoord >= options.maxCoord:
      print("Wrong min/max values!")
      raise ValueError

  def atomInChannel(coord):
    if coord <= options.maxCoord and coord >= options.minCoord:
      return True
    return False
 
  initials = {}
  permeating = {}
  atomCoords = {}
  isFirstFrame = True
  lastFrame = -1
  penultimateFrame = -1

  print("atomIndex\tframeIn\tcoordIn\tframeOut\tcoordOut")

  for atom in reader:
    frame = int(atom["frame"])
    index = int(atom["index"])
    coord = float(atom[options.axis])
    
    if isFirstFrame:
      firstFrame = frame
      isFirstFrame = False
      lastFrame = frame
      atomCoords[frame] = {}

    if frame == firstFrame:
      if atomInChannel(coord):
        initials[index] = coord
    else:
      if frame != lastFrame:
        checkForPermeations(initials,permeating,atomCoords,lastFrame,penultimateFrame,options.minCoord,options.maxCoord,options.minDist)
        penultimateFrame = lastFrame
        lastFrame = frame
        atomCoords[frame] = {}
      if atomInChannel(coord):
        atomCoords[frame][index] = coord

  checkForPermeations(initials,permeating,atomCoords,frame,penultimateFrame,options.minCoord,options.maxCoord,options.minDist)

main()
