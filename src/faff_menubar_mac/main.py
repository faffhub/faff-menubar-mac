import threading
import rumps
from PyObjCTools import AppHelper
from faff_core import Workspace, start_watching

ws = Workspace()


class FaffMenubar(rumps.App):
    def __init__(self):
        super().__init__("🧠", title="ﬀ: Resting...")
        self.menu = ["Stop", "Refresh"]
        self.update_title()
        t = threading.Thread(target=self._watch_events, daemon=True)
        t.start()

    def update_title(self, _=None):
        try:
            current_task = ws.logs.get_log(ws.today()).active_session()
            self.title = f"ﬀ: {current_task.alias}" if current_task else "ﬀ: Resting..."
        except Exception:
            self.title = "ﬀ: Error"

    def _watch_events(self):
        stream = start_watching("~/.faff")
        for event in stream:
            if event.event_type == "log_changed":
                AppHelper.callAfter(self.update_title)

    @rumps.clicked("Stop")
    def stop_session(self, _):
        current_task = ws.logs.get_log(ws.today()).active_session()
        if current_task:
            ws.logs.stop_current_session()
            self.update_title()
        else:
            rumps.notification("Faff", "No active session", "Nothing to stop.")

    @rumps.clicked("Refresh")
    def refresh(self, _):
        self.update_title()


def main():
    FaffMenubar().run()


if __name__ == "__main__":
    main()
