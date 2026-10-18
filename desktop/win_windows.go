//go:build windows

package main

import (
	"os"
	"runtime"
	"syscall"
	"unsafe"
)

var (
	comdlg32         = syscall.NewLazyDLL("comdlg32.dll")
	user32           = syscall.NewLazyDLL("user32.dll")
	pGetSaveFileName = comdlg32.NewProc("GetSaveFileNameW")
	pMessageBox      = user32.NewProc("MessageBoxW")
)

type openFileName struct {
	lStructSize       uint32
	hwndOwner         uintptr
	hInstance         uintptr
	lpstrFilter       *uint16
	lpstrCustomFilter *uint16
	nMaxCustFilter    uint32
	nFilterIndex      uint32
	lpstrFile         *uint16
	nMaxFile          uint32
	lpstrFileTitle    *uint16
	nMaxFileTitle     uint32
	lpstrInitialDir   *uint16
	lpstrTitle        *uint16
	flags             uint32
	nFileOffset       uint16
	nFileExtension    uint16
	lpstrDefExt       *uint16
	lCustData         uintptr
	lpfnHook          uintptr
	lpTemplateName    *uint16
	pvReserved        uintptr
	dwReserved        uint32
	flagsEx           uint32
}

func u16(s string) *uint16 { p, _ := syscall.UTF16PtrFromString(s); return p }

func msg(text string) {
	pMessageBox.Call(0, uintptr(unsafe.Pointer(u16(text))), uintptr(unsafe.Pointer(u16("Bikini Bottom Builder"))), 0x10)
}

// saveDialog shows the native Save As dialog and returns the chosen path ("" if cancelled).
func saveDialog(suggested string) string {
	runtime.LockOSThread()
	defer runtime.UnlockOSThread()
	buf := make([]uint16, 1024)
	copy(buf, syscall.StringToUTF16(suggested))
	filter := syscall.StringToUTF16("Game Boy Advance ROM (*.gba)\x00*.gba\x00All files (*.*)\x00*.*\x00")
	ofn := openFileName{
		lpstrFilter: &filter[0], nFilterIndex: 1, lpstrFile: &buf[0], nMaxFile: uint32(len(buf)),
		lpstrTitle: u16("Save edited ROM"), lpstrDefExt: u16("gba"),
		flags: 0x00000002 | 0x00000004 | 0x00000800 | 0x00080000, // OVERWRITEPROMPT | HIDEREADONLY | PATHMUSTEXIST | EXPLORER
	}
	ofn.lStructSize = uint32(unsafe.Sizeof(ofn))
	r, _, _ := pGetSaveFileName.Call(uintptr(unsafe.Pointer(&ofn)))
	if r == 0 {
		return ""
	}
	return syscall.UTF16ToString(buf)
}

func findBrowser() string {
	cands := []string{
		os.Getenv("ProgramFiles(x86)") + `\Microsoft\Edge\Application\msedge.exe`,
		os.Getenv("ProgramFiles") + `\Microsoft\Edge\Application\msedge.exe`,
		os.Getenv("ProgramFiles") + `\Google\Chrome\Application\chrome.exe`,
		os.Getenv("ProgramFiles(x86)") + `\Google\Chrome\Application\chrome.exe`,
		os.Getenv("LocalAppData") + `\Google\Chrome\Application\chrome.exe`,
	}
	for _, c := range cands {
		if _, err := os.Stat(c); err == nil {
			return c
		}
	}
	return ""
}

