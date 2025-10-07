import rumps
from faff.core import Workspace
from pathlib import Path

HOME = Path("/Users/tom/.faff/")

ws = Workspace(HOME)


class FaffMenubar(rumps.App):
    def __init__(self):
        super().__init__("🧠", title="ﬀ: Resting...")
        self.timer = rumps.Timer(self.update_title, 10)  # Update every 10 seconds
        self.menu = [
            "Stop"
        ]
        self.timer.start()

    def update_title(self, _=None):
        current_task = ws.logs.get_log(ws.today()).active_session()
        self.title = f"ﬀ: {current_task.intent.alias}" if current_task else "ﬀ: Resting..."

if __name__ == "__main__":
    FaffMenubar().run()
