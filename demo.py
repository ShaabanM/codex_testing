import json
import tkinter as tk
from tkinter import ttk

from agentlogontology import from_openai_trace


class LogViewer(tk.Tk):
    def __init__(self, log):
        super().__init__()
        self.title("Agent Log Viewer")
        self.log = log
        self._create_widgets()
        self._populate()

    def _create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("action", "object", "kind"), show="headings")
        self.tree.heading("action", text="Action")
        self.tree.heading("object", text="Object ID")
        self.tree.heading("kind", text="Object Kind")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.payload_text = tk.Text(self, height=10)
        self.payload_text.pack(fill=tk.BOTH, expand=True)

        self.save_btn = tk.Button(self, text="Save State", command=self._save)
        self.save_btn.pack(pady=4)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _populate(self):
        run = self.log.runs[0]
        for idx, event in enumerate(run.events):
            obj_id = event.action.target or ""
            obj_kind = run.objects.get(obj_id).kind.value if obj_id in run.objects else ""
            self.tree.insert("", "end", iid=str(idx), values=(event.action.kind.value, obj_id, obj_kind))

    def _on_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        event = self.log.runs[0].events[idx]
        obj = self.log.runs[0].objects.get(event.action.target)
        self.payload_text.delete("1.0", tk.END)
        if obj:
            self.payload_text.insert(tk.END, json.dumps(obj.state, indent=2))

    def _save(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        try:
            new_state = json.loads(self.payload_text.get("1.0", tk.END))
        except json.JSONDecodeError:
            return
        run = self.log.runs[0]
        event = run.events[idx]
        obj = run.objects.get(event.action.target)
        if obj:
            obj.state = new_state
            self.tree.item(sel[0], values=(event.action.kind.value, obj.object_id, obj.kind.value))


if __name__ == "__main__":
    with open("sample_agent_trace.json") as f:
        data = json.load(f)
    log = from_openai_trace(data)
    viewer = LogViewer(log)
    viewer.mainloop()
