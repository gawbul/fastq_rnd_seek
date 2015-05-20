#!/Applications/Julia-0.3.5.app/Contents/Resources/julia/bin/julia
# required modules
require("argparse")
using ArgParse

# parse arguments
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

# get random position in file
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
  println("$(infilesize)")
  
  # open input file
  infh = open(filename, "r")

  # iterate number of samples times
  for i = 1:numsamples
    pos = get_random_pos(infilesize)
    seek(infh, pos)
    println(pos)
    println(position(infh)) 
    println(readline(infh))
    exit()
  end

  # close file handle
  close(infh)
end

# call main function
main()

