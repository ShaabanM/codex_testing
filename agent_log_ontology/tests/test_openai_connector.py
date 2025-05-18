import json
import unittest
from pathlib import Path

from agent_log_ontology.connectors.openai_traces import from_openai_trace
from agent_log_ontology.ontology.run import AgentRun


class OpenAIConnectorTest(unittest.TestCase):
    def test_round_trip(self):
        sample_path = (
            Path(__file__).resolve().parent.parent / "samples" / "openai_example.json"
        )
        data = json.loads(sample_path.read_text())
        run = from_openai_trace(data)
        dumped = run.json()
        run2 = AgentRun.parse_raw(dumped)
        self.assertEqual(run.id, run2.id)
        self.assertEqual(len(run.steps), len(run2.steps))
        self.assertEqual(
            run.steps[0].messages[0].content, run2.steps[0].messages[0].content
        )


if __name__ == "__main__":
    unittest.main()
