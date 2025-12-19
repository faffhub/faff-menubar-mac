"""
Faff menubar app with event-driven updates.

Uses the faff-core event stream to get immediate updates when log files change,
instead of polling every 10 seconds.
"""

import rumps
import queue
import threading
from faff_core import Workspace, start_watching
from pathlib import Path

HOME = Path.home() / ".faff"

ws = Workspace()


class FaffMenubar(rumps.App):
    def __init__(self):
        super().__init__("🧠", title="ﬀ: Ready.")

        # Menu items
        self.menu = ["Stop", "Refresh"]

        # Event queue for thread-safe communication
        self.event_queue = queue.Queue()

        # Event watcher thread
        self.watcher_thread = None
        self.running = False

        # Initial update
        self.update_title()

        # Start event watcher
        self.start_event_watcher()

        # Poll event queue from main thread
        self.event_timer = rumps.Timer(self.check_events, 0.1)
        self.event_timer.start()

    def start_event_watcher(self):
        """Start the background event watcher thread."""
        self.running = True
        self.watcher_thread = threading.Thread(
            target=self._watch_events,
            daemon=True
        )
        self.watcher_thread.start()

    def _watch_events(self):
        """Background thread that watches for log file changes."""
        try:
            stream = start_watching(str(HOME))

            for event in stream:
                if not self.running:
                    break

                # Only update on log changes (not plan changes)
                if event.event_type == "log_changed":
                    # Queue the update to be processed on main thread
                    self.event_queue.put("update")

        except StopIteration:
            pass
        except Exception as e:
            print(f"Event watcher error: {e}")
            import traceback
            traceback.print_exc()

    def check_events(self, _):
        """Check event queue and process updates (runs on main thread)."""
        try:
            while True:
                event = self.event_queue.get_nowait()
                if event == "update":
                    self.update_title()
        except queue.Empty:
            pass

    def update_title(self, _=None):
        """Update the menubar title with current session info."""
        try:
            current_task = ws.logs.get_log(ws.today()).active_session()

            if current_task:
                alias = current_task.intent.alias or "Unknown"

                # Calculate elapsed time
                try:
                    elapsed_ms = current_task.elapsed()
                    if elapsed_ms:
                        hours = int(elapsed_ms / (1000 * 60 * 60))
                        minutes = int((elapsed_ms % (1000 * 60 * 60)) / (1000 * 60))
                        time_str = f" ({hours:02d}:{minutes:02d})"
                    else:
                        time_str = ""
                except:
                    time_str = ""

                self.title = f"ﬀ: {alias}{time_str}"
            else:
                self.title = "ﬀ: Ready."

        except Exception as e:
            self.title = f"ﬀ: Error"
            print(f"Error updating title: {e}")

    @rumps.clicked("Refresh")
    def refresh(self, _):
        """Manually refresh the menubar title."""
        self.update_title()

    @rumps.clicked("Stop")
    def stop_session(self, _):
        """Stop the current session."""
        try:
            current_task = ws.logs.get_log(ws.today()).active_session()
            if current_task:
                alias = current_task.intent.alias or "Unknown"
                ws.logs.stop_current_session()
                self.update_title()
                rumps.notification(
                    title="Faff",
                    subtitle="Session stopped",
                    message=f"Stopped: {alias}"
                )
            else:
                rumps.notification(
                    title="Faff",
                    subtitle="No active session",
                    message="There's no session to stop"
                )
        except Exception as e:
            rumps.notification(
                title="Faff Error",
                subtitle="Failed to stop session",
                message=str(e)
            )

    def cleanup(self):
        """Cleanup when app quits."""
        print("Cleaning up...")
        self.running = False
        if self.event_timer:
            self.event_timer.stop()
        if self.watcher_thread:
            self.watcher_thread.join(timeout=1)
        print("Cleanup complete")


def main():
    app = FaffMenubar()
    try:
        app.run()
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()
