#!/usr/bin/env ruby
puts "=== Log Processor Pipeline ==="
scripts = %w[append_to_log update_runfile archive_entries]
scripts.each do |script|
  puts "Running #{script}..."
  load File.join(__dir__, "scripts", "#{script}.rb")
  puts "  done."
end
puts "=== Pipeline complete ==="
