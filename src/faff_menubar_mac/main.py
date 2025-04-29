HOME = "/Users/tom/.faff/"

from faff.core import Workspace

ws = Workspace(HOME)

import rumps

class FaffMenubar(rumps.App):
    def __init__(self):
        super().__init__("🧠", title="ﬀ: Resting...")
        self.timer = rumps.Timer(self.update_title, 10)  # Update every 10 seconds
        self.timer.start()

    def update_title(self, _=None):
        current_task = ws.get_log(ws.today()).active_timeline_entry()
        self.title = f"ﬀ: {current_task.activity.name}" if current_task else "ﬀ: Resting..."

if __name__ == "__main__":
    FaffMenubar().run()
