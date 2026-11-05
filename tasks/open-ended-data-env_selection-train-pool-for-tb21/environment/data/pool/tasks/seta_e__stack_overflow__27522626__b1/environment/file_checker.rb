#!/usr/bin/env ruby
# file_checker.rb — simple file integrity checker.
#
# Usage:
#   ruby file_checker.rb index  <directory> [--manifest FILE]
#   ruby file_checker.rb check  <directory> [--manifest FILE]
#   ruby file_checker.rb dupes  <directory> [--manifest FILE]

require 'json'
require_relative 'hasher'

DEFAULT_MANIFEST = "manifest.json"

def cmd_index(directory, manifest_path)
  entries = {}
  Dir.glob(File.join(directory, '**', '*')).select { |f| File.file?(f) }.sort.each do |fpath|
    rel = fpath.sub(%r{\A#{Regexp.escape(directory)}/?}, '')
    entries[rel] = hash_file(fpath)
  end
  File.write(manifest_path, JSON.pretty_generate(entries.sort.to_h))
  puts "Indexed #{entries.size} file(s) -> #{manifest_path}"
end

def cmd_check(directory, manifest_path)
  manifest = JSON.parse(File.read(manifest_path))
  ok = changed = missing = 0
  manifest.sort.each do |rel, stored_fp|
    fpath = File.join(directory, rel)
    if !File.exist?(fpath)
      puts "MISSING  #{rel}"
      missing += 1
    elsif verify_against_stored(fpath, stored_fp)
      puts "OK       #{rel}"
      ok += 1
    else
      puts "CHANGED  #{rel}"
      changed += 1
    end
  end
  puts "\nSummary: #{ok} OK, #{changed} CHANGED, #{missing} MISSING"
end

def cmd_dupes(directory, manifest_path)
  manifest = JSON.parse(File.read(manifest_path))
  by_hash = {}
  manifest.each do |rel, fp|
    (by_hash[fp] ||= []) << rel
  end
  found = false
  by_hash.each do |fp, paths|
    if paths.length > 1
      found = true
      puts "Duplicate group (fingerprint #{fp[0..15]}...):"
      paths.sort.each { |p| puts "  #{p}" }
    end
  end
  puts "No duplicates found." unless found
end

# CLI parsing
command = ARGV[0]
directory = ARGV[1]
manifest = DEFAULT_MANIFEST

if (idx = ARGV.index('--manifest'))
  manifest = ARGV[idx + 1]
end

case command
when 'index'
  cmd_index(directory, manifest)
when 'check'
  cmd_check(directory, manifest)
when 'dupes'
  cmd_dupes(directory, manifest)
when '--help', '-h', nil
  puts <<~HELP
    Usage:
      ruby file_checker.rb index  <directory> [--manifest FILE]
      ruby file_checker.rb check  <directory> [--manifest FILE]
      ruby file_checker.rb dupes  <directory> [--manifest FILE]
  HELP
else
  $stderr.puts "Unknown command: #{command}"
  exit 1
end
