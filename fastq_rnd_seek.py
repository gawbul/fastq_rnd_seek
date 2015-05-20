#!/usr/bin/env python
# import modules
import os, random, sys

# parse arguments
if len(sys.argv) != 2:
  print "Requires one input filename as an argument."
  sys.exit()
filename = sys.argv[1]

# check file exists
if not os.path.exists(filename):
  print "Filename doesn't exist."
  sys.exit()

# define variables
record_positions = []
line_positions = {}

# open file
linenum = 0
length = 0
infh = open(filename, 'r')
for line in infh:
  line_positions[linenum] = length
  if line.startswith("@"):
    position = line_positions[linenum]
    record_positions.append(position)
  length += len(line)
  linenum += 1
infh.close()

# sort positions
record_positions = sorted(record_positions)
print "Number of records: %d" % len(record_positions)

# get random record
rnd_record = random.choice(record_positions) 
rnd_record_idx = record_positions.index(rnd_record)
# check that we haven't selected the last record at random
if rnd_record_idx == record_positions.index(record_positions[-1]):
  next_record = rnd_record
  rnd_record = record_positions[rnd_record_idx - 1]
else:
  next_record = record_positions[rnd_record_idx + 1]
print "Selected record positions: %d, %d" % (rnd_record, next_record)
print "Record length: %d" % (next_record - rnd_record)

# get average record lengths
record_lengths = []
for record in record_positions[:-1]:
  thispos = record
  nextpos = record_positions[record_positions.index(record) + 1]
  record_lengths.append(nextpos - thispos)
print "Average record length: %d" % sum(record_lengths) / len(record_lengths)

# read record
infh = open(filename, 'r')
infh.seek(rnd_record)
record = infh.read((next_record - rnd_record) - 1)
infh.close()

# display record
print "Seq:\n\n%s" % record
