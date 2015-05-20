#!/usr/bin/env python
# import modules
import mmap, os, random, sys
from Bio import SeqIO
from StringIO import StringIO

# parse arguments
if len(sys.argv) != 3:
  print "Requires an input filename and integer as arguments."
  sys.exit()
filename = sys.argv[1]
try:
  num_seqs = int(sys.argv[2])
except:
  print "Require a valid integer value for number of sequences to sample."
  sys.exit()

# check file exists
if not os.path.exists(filename):
  print "Filename %s doesn't exist." % filename
  sys.exit()

# get size of the file
filesize = os.path.getsize(filename)

# define variables
observed_offsets = []

# open file
with open(filename, 'rb') as infh:
  mm = mmap.mmap(infh.fileno(), 0, prot=mmap.PROT_READ)
  for i in range(num_seqs):
    failed = True
    while failed:
      # pick a random offset and seek to that position
      random_offset = random.randrange(filesize)
      mm.seek(random_offset)
      # always seek to a position where there is a record in the file
      if mm.rfind("\n@") == -1:
        continue
      # find the first record after the offset
      current_record_offset = mm.find("\n@") + 1
      # check not already seen this record
      if current_record_offset in observed_offsets:
        continue
      # add current record to list of observed records 
      observed_offsets.append(current_record_offset)
      # seek to current record and find the next
      mm.seek(current_record_offset)
      next_record_offset = mm.find("\n@")
      # check not already in the last record set as end of file if we are
      if next_record_offset == -1:
        next_record_offset = filesize
      # read record
      seq = mm.read(next_record_offset - current_record_offset)
      # check if is a valid sequence
      try:
        record = SeqIO.read(StringIO(seq), 'fastq')
      except:
        continue
      failed = False
  mm.close()
