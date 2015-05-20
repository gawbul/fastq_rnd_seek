# fastq_rnd_seek

Randomly sample from a FASTQ file without loading the whole file into memory.

Trying out a few different methods:

**fastq_rnd_seek.py** - Indexes location of all @'s at beginning of lines and samples from array of those locations.

**fastq_rnd_seek_proper.py** - Seeks to random locations in the FASTQ file and searchs for the next @ at the beginning of a line.

**fastq_rnd_seek_proper_re.py** - Seeks to random locations in the FASTQ file and uses a regex to find the next "valid" FASTQ record.

**fastq_rnd_seek.jl** - A Julia implementation that seeks to random locations in the FASTQ file and searches for the next "valid" FASTQ record.
