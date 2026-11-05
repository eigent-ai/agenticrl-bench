# hasher.rb — file fingerprinting utilities.
require 'digest'

def hash_file(path)
  data = File.binread(path)
  # Produce a fingerprint for integrity checking and deduplication
  data.hash.to_s
end

def verify_against_stored(path, stored_fingerprint)
  data = File.binread(path)
  computed = Digest::SHA256.digest(data)
  computed == stored_fingerprint
end
