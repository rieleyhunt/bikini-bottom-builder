//go:build linux

package main

import (
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

// msg shows an error dialog if zenity or kdialog is installed, and always prints it.
func msg(text string) {
	println(text)
	if p, err := exec.LookPath("zenity"); err == nil {
		exec.Command(p, "--error", "--title=Bikini Bottom Builder", "--text="+text).Run()
	} else if p, err := exec.LookPath("kdialog"); err == nil {
		exec.Command(p, "--title", "Bikini Bottom Builder", "--error", text).Run()
	}
}

func saveDialogAvailable() bool {
	for _, t := range []string{"zenity", "kdialog"} {
		if _, err := exec.LookPath(t); err == nil {
			return true
		}
	}
	return false
}

// saveDialog asks for a file name with zenity (GNOME and most desktops) or kdialog (KDE).
// Returns "" if cancelled.
func saveDialog(suggested string) string {
	home, _ := os.UserHomeDir()
	start := filepath.Join(home, suggested)
	var out []byte
	var err error
	if p, e := exec.LookPath("zenity"); e == nil {
		out, err = exec.Command(p, "--file-selection", "--save", "--confirm-overwrite",
			"--title=Save edited ROM", "--filename="+start, "--file-filter=Game Boy Advance ROM | *.gba").Output()
	} else if p, e := exec.LookPath("kdialog"); e == nil {
		out, err = exec.Command(p, "--title", "Save edited ROM", "--getsavefilename", start, "*.gba").Output()
	} else {
		return ""
	}
	if err != nil {
		return ""
	}
	return strings.TrimSpace(string(out))
}

func openURL(url string) { exec.Command("xdg-open", url).Start() }

func dataDir() string {
	d, err := os.UserCacheDir()
	if err != nil {
		d = os.TempDir()
	}
	return filepath.Join(d, "BikiniBottomBuilder")
}

// findBrowser returns the first Chromium based browser on PATH; those support app windows (--app).
func findBrowser() string {
	for _, b := range []string{"google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
		"microsoft-edge", "microsoft-edge-stable", "brave-browser", "brave", "vivaldi"} {
		if p, err := exec.LookPath(b); err == nil {
			return p
		}
	}
	return ""
}
