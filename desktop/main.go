// Bikini Bottom Builder desktop launcher (Windows and Linux).
// Serves the embedded editor on 127.0.0.1 and opens it in a Chromium based browser's app window
// (Edge or Chrome on Windows; Chrome, Chromium, Edge or Brave on Linux).
// Export uses the browser's save picker, with the system's own Save dialog as a fallback.
package main

import (
	_ "embed"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"sync"
	"time"
)

//go:embed index.html
var page []byte

var (
	lastPing = time.Now()
	byeAt    time.Time
	pingMu   sync.Mutex
)

func main() {
	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		msg("Could not start: " + err.Error())
		return
	}
	url := fmt.Sprintf("http://%s/", ln.Addr().String())
	if os.Getenv("BBB_DEBUG") != "" {
		println(url)
	}

	logPath := filepath.Join(dataDir(), "log.txt")
	os.MkdirAll(filepath.Dir(logPath), 0755)
	logf, _ := os.OpenFile(logPath, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0644)
	logLine := func(f string, a ...any) {
		if logf != nil {
			fmt.Fprintf(logf, time.Now().Format("15:04:05 ")+f+"\n", a...)
		}
	}
	logLine("started on %s", url)
	safe := func(h http.HandlerFunc) http.HandlerFunc {
		return func(w http.ResponseWriter, r *http.Request) {
			defer func() {
				if e := recover(); e != nil {
					logLine("panic in %s: %v", r.URL.Path, e)
					w.WriteHeader(500)
				}
			}()
			h(w, r)
		}
	}
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.Header().Set("Cache-Control", "no-store")
		w.Write(page)
	})
	mux.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {
		pingMu.Lock(); lastPing = time.Now(); pingMu.Unlock()
		w.WriteHeader(204)
	})
	mux.HandleFunc("/bye", func(w http.ResponseWriter, r *http.Request) {
		pingMu.Lock(); byeAt = time.Now(); pingMu.Unlock()
		w.WriteHeader(204)
	})
	mux.HandleFunc("/save", safe(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			w.WriteHeader(405); return
		}
		data, err := io.ReadAll(r.Body)
		w.Header().Set("Content-Type", "application/json")
		if err != nil || len(data) == 0 {
			json.NewEncoder(w).Encode(map[string]any{"ok": false, "error": "No ROM data received."}); return
		}
		name := filepath.Base(r.URL.Query().Get("name"))
		if !saveDialogAvailable() {
			json.NewEncoder(w).Encode(map[string]any{"ok": false, "nodialog": true}); return
		}
		path := saveDialog(name)
		if path == "" {
			json.NewEncoder(w).Encode(map[string]any{"ok": false, "cancelled": true}); return
		}
		if err := os.WriteFile(path, data, 0644); err != nil {
			json.NewEncoder(w).Encode(map[string]any{"ok": false, "error": err.Error()}); return
		}
		logLine("saved %d bytes to %s", len(data), path)
		json.NewEncoder(w).Encode(map[string]any{"ok": true, "path": path})
	}))
	go http.Serve(ln, mux)

	profile := filepath.Join(dataDir(), "window")
	opened := false
	if b := findBrowser(); b != "" {
		cmd := exec.Command(b, "--app="+url, "--user-data-dir="+profile, "--window-size=1440,900",
			"--no-first-run", "--no-default-browser-check", "--disable-features=Translate")
		opened = cmd.Start() == nil
	}
	if !opened {
		openURL(url)
	}
	// Edge's launcher process can exit straight away, so the window's lifetime is tracked from the
	// page itself: it pings every few seconds and says goodbye when it closes.
	for {
		time.Sleep(time.Second)
		pingMu.Lock()
		idle, bye, lp := time.Since(lastPing), byeAt, lastPing
		pingMu.Unlock()
		if !bye.IsZero() && bye.After(lp) && time.Since(bye) > 5*time.Second {
			logLine("window closed, exiting")
			return // window closed and nothing reconnected (a refresh would have pinged again)
		}
		if idle > 3*time.Minute {
			logLine("no ping for 3 minutes, exiting")
			return // window gone without saying goodbye
		}
	}
}
