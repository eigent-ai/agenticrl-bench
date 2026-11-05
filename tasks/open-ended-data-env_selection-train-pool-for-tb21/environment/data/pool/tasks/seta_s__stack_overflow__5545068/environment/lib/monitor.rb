# lib/monitor.rb
# Returns true if the given file path appears to be open in this Ruby process.
def file_open?(path)
  f = File.new(path)
  !f.closed?
end
