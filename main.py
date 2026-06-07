"""
main.py — TUESDAY Mobile
========================
Kivy entry point. Manages screen routing, async loop,
and the shared AgentOrchestrator instance.

FIXES vs original:
  - brain.initialise() now called properly after loop starts
  - MDNavigationBar API updated for KivyMD 2.x
  - Loop/brain init race condition resolved
  - memory_drive imported from correct relative path
"""
import asyncio
import os
import sys
import threading

from dotenv import load_dotenv
load_dotenv()

# Ensure agent/ tools/ screens/ are importable
sys.path.insert(0, os.path.dirname(__file__))

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem

from screens.chat_screen    import ChatScreen
from screens.memory_screen  import MemoryScreen
from screens.planner_screen import PlannerScreen
from screens.profile_screen import ProfileScreen

from agent.orchestrator import AgentOrchestrator
from memory_drive       import MemoryDrive

# ── Colour palette ────────────────────────────────────────────────────────────
BG_MAIN = (15/255, 17/255, 21/255, 1)
ACCENT  = (20/255, 184/255, 166/255, 1)


class TuesdayMobile(MDApp):

    def build(self):
        self.theme_cls.theme_style     = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.title = "TUESDAY"

        # ── 1. Start the persistent async event loop FIRST ────────────────────
        self.loop = asyncio.new_event_loop()
        loop_ready = threading.Event()

        def _run_loop():
            asyncio.set_event_loop(self.loop)
            self.loop.call_soon(loop_ready.set)   # signal when loop is live
            self.loop.run_forever()

        threading.Thread(target=_run_loop, daemon=True).start()
        loop_ready.wait(timeout=5)   # wait until loop is actually running

        # ── 2. Init shared brain AFTER loop is confirmed live ─────────────────
        self.memory = MemoryDrive()
        self.brain  = AgentOrchestrator()

        # Call brain.initialise() on the running loop and wait for it
        future = asyncio.run_coroutine_threadsafe(
            self.brain.initialise(), self.loop)
        try:
            future.result(timeout=15)
        except Exception as e:
            print(f"[TUESDAY] Brain init warning: {e}")

        # ── 3. Build UI ───────────────────────────────────────────────────────
        root = MDBoxLayout(orientation="vertical", md_bg_color=BG_MAIN)

        self.sm = ScreenManager(transition=NoTransition())
        for Screen, name in [
            (ChatScreen,    "chat"),
            (MemoryScreen,  "memory"),
            (PlannerScreen, "planner"),
            (ProfileScreen, "profile"),
        ]:
            self.sm.add_widget(Screen(app=self, name=name))

        root.add_widget(self.sm)

        # ── Bottom navigation bar (KivyMD 2.x API) ───────────────────────────
        self._nav_map = {
            "Chat":    "chat",
            "Memory":  "memory",
            "Planner": "planner",
            "Profile": "profile",
        }
        nav = MDNavigationBar()
        nav.bind(on_switch_tabs=self._on_tab_switch)
        for icon, label in [
            ("message-text-outline",  "Chat"),
            ("brain",                 "Memory"),
            ("calendar-check",        "Planner"),
            ("account-outline",       "Profile"),
        ]:
            nav.add_widget(MDNavigationItem(
                icon=icon, text=label))
        root.add_widget(nav)

        return root

    def _on_tab_switch(self, bar, item, item_icon, item_text):
        """KivyMD 2.x navigation callback."""
        self.sm.current = self._nav_map.get(item_text, "chat")

    def on_stop(self):
        """Clean shutdown — stop the async loop."""
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)


if __name__ == "__main__":
    TuesdayMobile().run()
