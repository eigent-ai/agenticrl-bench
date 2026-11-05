package fileops

import (
	"fmt"
	"os"
	"path/filepath"
)

// DeleteRecursively removes dir and all of its contents.
// Returns nil if dir doesn't exist or was successfully removed.
func DeleteRecursively(dir string) error {
	if dir == "" {
		return nil
	}
	info, err := os.Stat(dir)
	if os.IsNotExist(err) {
		return nil
	}
	if err != nil {
		return err
	}
	if !info.IsDir() {
		return os.Remove(dir)
	}
	entries, err := os.ReadDir(dir)
	if err != nil {
		return err
	}
	for _, entry := range entries {
		os.Remove(filepath.Join(dir, entry.Name()))
	}
	return os.Remove(dir)
}

// CleanContents removes all contents of dir but keeps the dir itself.
// Returns nil if dir exists and is empty after the call.
func CleanContents(dir string) error {
	if dir == "" {
		return fmt.Errorf("empty path")
	}
	info, err := os.Stat(dir)
	if err != nil {
		return err
	}
	if !info.IsDir() {
		return fmt.Errorf("not a directory: %s", dir)
	}
	if err := DeleteRecursively(dir); err != nil {
		return err
	}
	return os.MkdirAll(dir, 0755)
}
