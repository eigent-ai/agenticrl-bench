# Reads the current run count and increments it in-place
File.open("/opt/logprocessor/data/runfile.txt", "r") do |f|
  count = f.read.strip.to_i
  count += 1
  f.seek(0)
  f.truncate(0)
  f.write(count.to_s)
end
