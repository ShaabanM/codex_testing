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
        self.tree = ttk.Treeview(self, columns=("type", "payload"), show="headings")
        self.tree.heading("type", text="Event Type")
        self.tree.heading("payload", text="Payload")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.payload_text = tk.Text(self, height=10)
        self.payload_text.pack(fill=tk.BOTH, expand=True)

        self.save_btn = tk.Button(self, text="Save Payload", command=self._save)
        self.save_btn.pack(pady=4)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _populate(self):
        run = self.log.runs[0]
        for idx, event in enumerate(run.events):
            self.tree.insert("", "end", iid=str(idx), values=(event.event_type, json.dumps(event.payload)))

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        event = self.log.runs[0].events[idx]
        self.payload_text.delete("1.0", tk.END)
        self.payload_text.insert(tk.END, json.dumps(event.payload, indent=2))

    def _save(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        try:
            new_payload = json.loads(self.payload_text.get("1.0", tk.END))
        except json.JSONDecodeError:
            return
        event = self.log.runs[0].events[idx]
        event.payload = new_payload
        self.tree.item(sel[0], values=(event.event_type, json.dumps(event.payload)))


if __name__ == "__main__":
    with open("sample_agent_trace.json") as f:
        data = json.load(f)
    log = from_openai_trace(data)
    viewer = LogViewer(log)
    viewer.mainloop()
