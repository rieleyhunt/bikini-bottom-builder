//go:build !windows && !linux

package main

import (
	"os"
	"path/filepath"
)

// Stubs so the server logic builds and can be tested on other systems.
func msg(text string)                    { println(text) }
func saveDialogAvailable() bool          { return os.Getenv("BBB_TEST_SAVE") != "" }
func saveDialog(suggested string) string { return os.Getenv("BBB_TEST_SAVE") }
func findBrowser() string                { return "" }
func openURL(url string)                 { println(url) }
func dataDir() string                    { return filepath.Join(os.TempDir(), "BikiniBottomBuilder") }
