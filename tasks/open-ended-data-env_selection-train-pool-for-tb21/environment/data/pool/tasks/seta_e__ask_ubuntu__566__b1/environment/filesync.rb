#!/usr/bin/env ruby
# File synchronization script that copies files to mounted destinations.
# Reads mount configuration from YAML and applies appropriate permission handling.

require 'yaml'
require 'fileutils'
require 'etc'

SOURCE_DIR = "/data/source"
CONFIG_FILE = "/opt/sync/mount_config.yml"
LOG_FILE = "/var/log/filesync/sync.log"

def log_msg(message)
  timestamp = Time.now.strftime("%Y-%m-%d %H:%M:%S")
  File.open(LOG_FILE, "a") { |f| f.puts "[#{timestamp}] #{message}" }
  puts "[#{timestamp}] #{message}"
end

def load_config
  if File.exist?(CONFIG_FILE)
    YAML.load_file(CONFIG_FILE) || {"mounts" => {}}
  else
    {"mounts" => {}}
  end
end

def parse_mode(mode_value, default_mode)
  # Parse mode value from config.
  # Expects an integer whose decimal digits represent octal permission bits.
  # e.g., 755 (decimal) -> "755" -> 0755 octal (0o755 = 493 decimal)
  # WARNING: If YAML parses 0755 as octal, we get 493 decimal, and
  # "493".to_i(8) will silently produce wrong results or raise an error!
  return default_mode if mode_value.nil?
  if mode_value.is_a?(String)
    mode_value.to_i(8)
  elsif mode_value.is_a?(Integer)
    mode_value.to_s.to_i(8)
  else
    default_mode
  end
end

def sync_files
  log_msg("Starting file synchronization...")
  config = load_config

  destinations = [
    {"path" => "/mnt/vfat_backup", "type" => "vfat"},
    {"path" => "/mnt/nfs_share", "type" => "nfs"}
  ]

  destinations.each do |dest_info|
    dest_path = dest_info["path"]
    dest_type = dest_info["type"]

    unless Dir.exist?(dest_path)
      log_msg("Warning: Destination #{dest_path} does not exist, skipping")
      next
    end

    log_msg("Syncing to #{dest_path} (type: #{dest_type})")

    mount_config = (config["mounts"] || {})[dest_path] || {}

    Dir.glob(File.join(SOURCE_DIR, "*")).each do |src_file|
      next unless File.file?(src_file)
      basename = File.basename(src_file)
      dest_file = File.join(dest_path, basename)

      begin
        FileUtils.cp(src_file, dest_file, preserve: false)

        if mount_config.any?
          if basename.end_with?('.sh')
            mode = parse_mode(mount_config["exec_mode"], 0755)
          else
            mode = parse_mode(mount_config["file_mode"], 0644)
          end

          uid = mount_config.fetch("uid", 0)
          gid = mount_config.fetch("gid", 0)

          File.chmod(mode, dest_file)
          File.chown(uid, gid, dest_file)
          log_msg("Applied configured permissions to #{basename}")
        else
          # Without config, simulate VFAT/NFS default behavior:
          if dest_type == "vfat"
            # Simulate VFAT without umask - files non-executable
            File.chmod(0600, dest_file)
          elsif dest_type == "nfs"
            # Simulate NFS with root_squash mapping - root ownership
            File.chown(0, 0, dest_file)
            File.chmod(0644, dest_file)
          end
          log_msg("Copied #{basename} (no mount config - default behavior)")
        end
      rescue => e
        log_msg("Error copying #{basename}: #{e.message}")
      end
    end
  end

  log_msg("Synchronization complete")
  0
end

exit(sync_files)
