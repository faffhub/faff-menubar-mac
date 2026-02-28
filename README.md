# faff-menubar-mac
A simple service to render the current task in the menubar.

## Installation

Install into your faff virtualenv:

```sh
pip install -e .
```

Then register and start the LaunchAgent:

```sh
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.tom.faff-menubar.plist
```

## Usage

```sh
# Restart (after code changes)
launchctl kickstart -k gui/$(id -u)/com.tom.faff-menubar

# Stop
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.tom.faff-menubar.plist

# Start
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.tom.faff-menubar.plist

# Check logs
tail -f ~/Library/Logs/faff-menubar.log
```

The LaunchAgent starts automatically at login and restarts if it crashes.

Since the package is installed in editable mode, changes to source files take effect after restarting the agent.
