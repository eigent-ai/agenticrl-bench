class FileCopier
  def self.copy(src, dest)
    content = File.open(src, "r") { |f| f.read }
    content = content.encode("UTF-8", invalid: :replace, undef: :replace)
    File.open(dest, "w") { |f| f.write(content) }
  end
end
