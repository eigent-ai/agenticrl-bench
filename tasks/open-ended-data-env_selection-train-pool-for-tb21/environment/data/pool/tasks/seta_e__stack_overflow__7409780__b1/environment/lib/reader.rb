module LogAnalyzer
  module Reader
    def self.read_header(path)
      File.open(path).readline.strip
    end

    def self.read_config(path)
      File.open(path, 'r').read
    end
  end
end
