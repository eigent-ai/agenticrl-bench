module LogAnalyzer
  module Scanner
    def self.scan_files(directory)
      paths = Dir.glob(File.join(directory, '*.log'))
      handles = paths.map { |p| File.open(p) }
      valid = paths.zip(handles)
                   .select { |_p, h| h.readline.start_with?('LOG') }
                   .map(&:first)
      valid.sort
    end
  end
end
