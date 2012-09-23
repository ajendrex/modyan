#!/usr/bin/env python3

# Written by Hector Urbina
# <hurbinas@gmail.com>

import sys
import argparse
import numpy
from csv import DictReader
import copy

def getSD(survivors,frameDict,baseFrame,stopFrame,N):
  if N == 0:
    return 0.0
  sdSum = 0
  for survivor in survivors:
    startCoords = frameDict[baseFrame][survivor]
    stopCoords = frameDict[stopFrame][survivor]
    sdSum += numpy.linalg.norm(stopCoords-startCoords)**2
  return sdSum / N

def getSurvivors(survivors,frameDict,startFrame,stopFrame):
  for i in range(stopFrame,startFrame,-1):
    survivors = [survivor for survivor in survivors if survivor in frameDict[i]]
  return survivors

def survivalTime(baseFrame, maxTau, tauList, frameDict, SD, Ptau):
  survivors = list(frameDict[baseFrame].keys())
  N = len(survivors)
  startFrame = baseFrame
  for i in range(baseFrame + 1,baseFrame + maxTau + 1):
    tau = i - baseFrame
    if tau in tauList:
      if N == 0:
        SD[tau][baseFrame] = 0.0
        Ptau[tau][baseFrame] = 0.0
      else:
        survivors = getSurvivors(survivors,frameDict,startFrame,i)
        SD[tau][baseFrame] = getSD(survivors,frameDict,baseFrame,i,N)
        Ptau[tau][baseFrame] = float(len(survivors)) / N
      startFrame = i

def main():

  commandLineParser = argparse.ArgumentParser(description="Calculates Mean Square Displacement and Survival Times for atoms in a trajectory. Formulas according to Liu et.al. 2004.")
  commandLineParser.add_argument('atomInfoFile', help='Atoms info file. Tab Separated Values: frame index x y z')
  commandLineParser.add_argument('tau', nargs='+', type=int, help='List of dt to evaluate, in picoseconds')
  commandLineParser.add_argument('-T', '--time', dest="maxT", default=1000000, type=int, help='Maximum time to evaluate, in picoseconds. Default: 1000000')
  commandLineParser.add_argument('-s', '--step', dest="timestep", default=1, type=int, help='Time Step value for every frame, in picoseconds. Default: 1')
  commandLineParser.add_argument('-a', '--axis', dest="axis", nargs='+', default=['x','y','z'], choices='xyz', help='Time Step value for every frame, in picoseconds. Default: 1')
  options = commandLineParser.parse_args()

  try:
    f = open(options.atomInfoFile, "r")
  except IOError:
    print("Couldn't open " + atomInfoFile)
  reader = DictReader(f, delimiter='\t')

  options.tau.sort()
  for tau in options.tau:
    if tau % options.timestep != 0:
      print("Wrong tau or timestep values. Tau values should be divisible by timestep!")
      raise ValueError
  options.tau = [int(x) for x in list(numpy.array(options.tau) / options.timestep)]
  tauList = copy.deepcopy(options.tau)
  maxTau = options.tau[-1]
  baseFrame = -1
  firstFrame = -1

  frameDict = {}
  SD = {}
  Ptau = {}
  for tau in options.tau:
    SD[tau] = {}
    Ptau[tau] = {}
  
  SDSum = {}
  PtauSum = {}

  print("t",end="")
  for tau in tauList:
    SDSum[tau] = 0
    PtauSum[tau] = 0
    print("\tSD(" + str(tau*options.timestep) + ")\tP(" + str(tau*options.timestep) + ")", end="")
  print()
  
  for atom in reader:
    frame = int(atom["frame"])
    index = int(atom["index"])
    x = float(atom["x"])
    y = float(atom["y"])
    z = float(atom["z"])
    
    if baseFrame == -1:
      baseFrame = frame
      firstFrame = frame
    
    if frame not in frameDict:
      for f in range(frame,0,-1):
        if f not in frameDict:
          frameDict[f] = {}
        else:
          break
      if frame - baseFrame > maxTau:
        for baseFrame in range(baseFrame,frame-maxTau):
          survivalTime(baseFrame,maxTau,options.tau,frameDict,SD,Ptau)
          print(str(baseFrame*options.timestep), end="")
          for tau in tauList:
            sd = SD[tau][baseFrame]
            p = Ptau[tau][baseFrame]
            SDSum[tau] += sd
            PtauSum[tau] += p
            print("\t" + str(sd) + "\t" + str(p), end="")
          print()
          sys.stdout.flush()
          del frameDict[baseFrame]
        baseFrame += 1
      if baseFrame > options.maxT / options.timestep:
        break

    D = frameDict[frame]
    # Here you can remove the coordinates you don't want to consider :)
    axisArray = []
    if 'x' in options.axis:
      axisArray.append(x)
    if 'y' in options.axis:
      axisArray.append(y)
    if 'z' in options.axis:
      axisArray.append(z)
    D[index] = numpy.array(axisArray)
      
  # If previously we got to the end of the file we still have to print the last line
  if frame - baseFrame == maxTau and baseFrame <= options.maxT / options.timestep:
    for baseFrame in range(baseFrame,frame+1-maxTau):
      survivalTime(baseFrame,maxTau,options.tau,frameDict,SD,Ptau)
      print(str(baseFrame*options.timestep), end="")
      for tau in tauList:
        sd = SD[tau][baseFrame]
        p = Ptau[tau][baseFrame]
        SDSum[tau] += sd
        PtauSum[tau] += p
        print("\t" + str(sd) + "\t" + str(p), end="")
      print()
      sys.stdout.flush()
    baseFrame += 1

  T = baseFrame - firstFrame

  print("Averages", end="")
  for tau in tauList:
    MSDtau = float(SDSum[tau]) / T 
    Ptau = float(PtauSum[tau]) / T
    print("\t" + str(MSDtau) + "(T=" + str(T) + ")\t" + str(Ptau) + "(T=" + str(T) + ")", end="")
  print()

main()
