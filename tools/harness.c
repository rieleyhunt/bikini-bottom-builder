// Minimal scriptable mGBA harness, driven from Python via ctypes.
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba/core/config.h>
#include <mgba/debugger/debugger.h>
#include <mgba-util/vfs.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static struct mCore* core;
static uint32_t vbuf[240 * 160];
static struct mDebugger* dbg;

#define MAXHITS 65536
struct hit { uint32_t addr, oldv, newv, pc, lr, r[13], kind, frame; };
static struct hit hits[MAXHITS];
static int nhits;
static int stopOnHit;
static volatile int stopped;

static void nolog(struct mLogger* l, int c, enum mLogLevel lv, const char* f, va_list a) {}
static struct mLogger quiet = { .log = nolog };

static uint32_t reg(const char* n) { int32_t v = 0; core->readRegister(core, n, &v); return v; }

static void entered(struct mDebugger* d, enum mDebuggerEntryReason reason, struct mDebuggerEntryInfo* info) {
	if (nhits < MAXHITS) {
		struct hit* h = &hits[nhits++];
		h->addr = info ? info->address : 0;
		h->kind = reason;
		if (info && reason == DEBUGGER_ENTER_WATCHPOINT) { h->oldv = info->type.wp.oldValue; h->newv = info->type.wp.newValue; }
		h->pc = reg("pc"); h->lr = reg("lr");
		char nm[4];
		for (int i = 0; i < 13; i++) { snprintf(nm, 4, "r%d", i); h->r[i] = reg(nm); }
		h->frame = core->frameCounter(core);
	}
	if (stopOnHit) stopped = 1;
	d->state = DEBUGGER_RUNNING;
}
static void paused(struct mDebugger* d) { d->state = DEBUGGER_RUNNING; }

int bf_init(const char* path) {
	mLogSetDefaultLogger(&quiet);
	core = mCoreFind(path);
	if (!core) return -1;
	core->init(core);
	mCoreInitConfig(core, NULL);
	core->setVideoBuffer(core, (color_t*) vbuf, 240);
	if (!mCoreLoadFile(core, path)) return -2;
	core->setAudioBufferSize(core, 2048);
	core->reset(core);
	return 0;
}

static int frameStart;
void bf_run(int frames, uint32_t keys) {
	core->setKeys(core, keys);
	for (int i = 0; i < frames; i++) {
		if (dbg) {
			uint32_t f = core->frameCounter(core);
			stopped = 0;
			while (core->frameCounter(core) == f && !stopped) {
				mDebuggerRun(dbg);
				if (dbg->state == DEBUGGER_PAUSED) dbg->state = DEBUGGER_RUNNING;
			}
			if (stopped) return;
		} else {
			core->runFrame(core);
		}
	}
}

uint32_t bf_r8(uint32_t a) { return core->busRead8(core, a); }
uint32_t bf_r16(uint32_t a) { return core->busRead16(core, a); }
uint32_t bf_r32(uint32_t a) { return core->busRead32(core, a); }
void bf_w8(uint32_t a, uint8_t v) { core->busWrite8(core, a, v); }
void bf_w16(uint32_t a, uint16_t v) { core->busWrite16(core, a, v); }
void bf_w32(uint32_t a, uint32_t v) { core->busWrite32(core, a, v); }
void bf_readblk(uint32_t a, uint32_t n, uint8_t* out) { for (uint32_t i = 0; i < n; i++) out[i] = core->busRead8(core, a + i); }
// rawWrite to patch ROM in-memory
void bf_romw8(uint32_t a, uint8_t v) { core->rawWrite8(core, a, -1, v); }
int bf_statesize(void) { return core->stateSize(core); }
int bf_save(void* b) { return core->saveState(core, b); }
int bf_load(void* b) { return core->loadState(core, b); }
uint32_t* bf_vbuf(void) { return vbuf; }
uint32_t bf_reg(const char* n) { return reg(n); }
uint32_t bf_frame(void) { return core->frameCounter(core); }

static void ensuredbg(void) {
	if (dbg) return;
	dbg = calloc(1, sizeof(*dbg));
	dbg->type = DEBUGGER_CUSTOM;
	dbg->entered = entered;
	dbg->paused = paused;
	mDebuggerAttach(dbg, core);
	dbg->state = DEBUGGER_RUNNING;
}
int bf_watch(uint32_t addr, int type) {
	ensuredbg();
	struct mWatchpoint w = { .address = addr, .segment = -1, .type = type };
	return dbg->platform->setWatchpoint(dbg->platform, &w);
}
int bf_break(uint32_t addr) {
	ensuredbg();
	struct mBreakpoint b = { .address = addr, .segment = -1, .type = BREAKPOINT_HARDWARE };
	return dbg->platform->setBreakpoint(dbg->platform, &b);
}
int bf_clearpoint(int id) { return dbg->platform->clearBreakpoint(dbg->platform, id); }
void bf_stoponhit(int s) { stopOnHit = s; }
int bf_nhits(void) { return nhits; }
struct hit* bf_hits(void) { return hits; }
void bf_clearhits(void) { nhits = 0; }
