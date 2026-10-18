//go:build !windows

package main

import "os"

// Test stubs so the server logic can be exercised off Windows.
func msg(text string)                 { println(text) }
func saveDialog(suggested string) string { return os.Getenv("BBB_TEST_SAVE") }
func findBrowser() string             { return "" }
