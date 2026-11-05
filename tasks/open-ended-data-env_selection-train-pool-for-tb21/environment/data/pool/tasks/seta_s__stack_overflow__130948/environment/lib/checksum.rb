require 'digest'

class Checksum
  def self.compute(path)
    content = File.read(path)
    Digest::SHA256.hexdigest(content)
  end
end
