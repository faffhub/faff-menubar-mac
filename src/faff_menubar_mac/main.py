import threading
import rumps
from PyObjCTools import AppHelper
from faff_core import Workspace, start_watching

ws = Workspace()


class FaffMenubar(rumps.App):
    def __init__(self):
        super().__init__("🧠", title="ﬀ: Resting...")
        self.menu = ["Stop"]
        self.update_title()
        t = threading.Thread(target=self._watch_events, daemon=True)
        t.start()

    def update_title(self):
        current_task = ws.logs.get_log(ws.today()).active_session()
        self.title = f"ﬀ: {current_task.intent.alias}" if current_task else "ﬀ: Resting..."

    def _watch_events(self):
        stream = start_watching("~/.faff")
        for event in stream:
            if event.event_type == "log_changed":
                AppHelper.callAfter(self.update_title)


def main():
    FaffMenubar().run()


if __name__ == "__main__":
    main()
