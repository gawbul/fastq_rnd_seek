#!/Applications/Julia-0.3.8.app/Contents/Resources/julia/bin/julia
# required modules
require("argparse")
using ArgParse

# function to parse arguments
function parse_arguments()
  s = ArgParseSettings()
  @add_arg_table s begin
    "filename"
      help = "Input filename."
      required = true
    "numsamples"
      help = "Number of sequences to sample."
      arg_type = Int
      default = 10000
  end
  return parse_args(s)
end

# function to return random position in file
function get_random_pos(rnd_num)
  return rand(0:rnd_num)
end

# main function
function main()
  # retrieve parsed arguments
  parsed_args = parse_arguments()

  # set filename
  filename = parsed_args["filename"]
  numsamples = parsed_args["numsamples"]

  # check file exists
  if !isfile(filename)
    throw(LoadError("", 0, "Filename $(filename) not found."))
  end

  # get file size
  infilesize = filesize(filename)

  # open input file
  infh = open(filename, "r")

  # iterate number of samples times
  for i = 1:numsamples
    valid_record = false
    lines = Array(ASCIIString, 4)
    while !valid_record
      pos = get_random_pos(infilesize)
      seek(infh, pos)
      readuntil(infh, "\n@")
      pos = position(infh) - 1
      seek(infh, pos)
      for j in [1:4]
        lines[j] = rstrip(readline(infh))
      end
      if beginswith(lines[1], "@") && beginswith(lines[3], "+")
        valid_record = true
      end
    end
    println(join(lines, "\n"))
  end

  # close file handle
  close(infh)
end

# call main function
main()
