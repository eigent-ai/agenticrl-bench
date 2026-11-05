# lib/streamer.rb
# Streams a file in fixed-size binary chunks, yielding each chunk to the caller.
def stream_file(filename, chunk_size = 1024)
  File.open(filename, 'rb') do |file|
    while (buffer = file.read(chunk_size))
      yield buffer
    end
  end
end

# Demo / smoke-test — streams the default sample file
stream_file('data/sample.bin')
