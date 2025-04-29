from datetime import datetime
from ansible.plugins.callback.default import CallbackModule as DefaultCallbackModule
from ansible.utils.color import stringc

class CallbackModule(DefaultCallbackModule):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'pretty_output'
    CALLBACK_NEEDS_WHITELIST = True

    def _time(self):
        return stringc(f"[{datetime.now().strftime('%H:%M:%S')}]", "white")
    
    def banner(self, msg):
      line_char = "-"  # or "═", "—", etc.
      width = 100
      fill_len = max(0, width - len(msg) - 1)
      return f"{msg} {line_char * fill_len}"

    def v2_playbook_on_start(self, playbook):
        self._display.display(self.banner(stringc("📚 Starting Playbook", "blue")))

    def v2_playbook_on_play_start(self, play):
        name = play.get_name().strip() or "Unnamed Play"
        self._display.display(self.banner(f"{self._time()} 📦 Play: {stringc(name, 'cyan')}"))

    def v2_playbook_on_task_start(self, task, is_conditional):
        name = task.get_name().strip() or "Unnamed Task"
        self._display.display(f"{self._time()} 📄 Task: {stringc(name, 'white')}")

    def v2_runner_on_start(self, host, task):
        task_name = task.get_name().strip() or "Unnamed Task"
        self._display.display(f"{self._time()} 🧪 Running on {host}: {task_name}")

    def v2_runner_on_ok(self, result):
        task_name = result._task.get_name()
        self._display.display(f"{self._time()} 🟢 OK: {stringc(task_name, 'green')}")

    def v2_runner_on_failed(self, result, ignore_errors=False):
        task_name = result._task.get_name()
        self._display.display(f"{self._time()} 🔴 FAILED: {stringc(task_name, 'red')}")
        if result._result.get('msg'):
            self._display.display(stringc(f"🔥 ERROR: {result._result['msg']}", "red"))

    def v2_runner_on_skipped(self, result):
        task_name = result._task.get_name()
        self._display.display(f"{self._time()} ⚪ SKIPPED: {stringc(task_name, 'magenta')}")

    def v2_playbook_on_stats(self, stats):
        self._display.display(self.banner(stringc("🏁 Playbook Complete", "green")))
        hosts = sorted(stats.processed.keys())
        for host in hosts:
            s = stats.summarize(host)
            summary = (
                f"{self._time()} 📋 {host}: "
                f"🟢 ok={stringc(str(s['ok']), 'green')} "
                f"🔁 changed={stringc(str(s['changed']), 'yellow')} "
                f"⚪ skipped={stringc(str(s['skipped']), 'magenta')} "
                f"🔴 failed={stringc(str(s['failures']), 'red')} "
                f"💀 unreachable={stringc(str(s['unreachable']), 'red')}"
            )
            self._display.display(summary)
