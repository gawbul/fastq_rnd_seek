#!/usr/bin/env python
# import modules
import mmap, os, random, re, sys

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
chunk_size = 4096

# define FASTQ regex
pattern = re.compile(r'@.+[\n\r]+[A-Z-]+[\n\r]+\+[\n\r]+.+[\n\r]{0,1}')

# open file
with open(filename, 'rb') as infh:
  mm = mmap.mmap(infh.fileno(), 0, prot=mmap.PROT_READ)
  for i in range(num_seqs):
    match = None
    while not match:
      # pick a random offset and seek to that position
      random_offset = random.randrange(filesize)
      mm.seek(random_offset)
      # read in a chunk of the file
      if not random_offset <= filesize - chunk_size:
        continue
      chunk = mm.read(chunk_size)
      match = re.search(pattern, chunk)
      if not match:
        continue
      start, end = match.span()
      record_offset = start
      record = chunk[start:end]
      # check not already seen this record
      if record_offset in observed_offsets:
        continue
      # add current record to list of observed records 
      observed_offsets.append(record_offset)
  mm.close()
