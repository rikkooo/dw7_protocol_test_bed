import unittest
import os
import json
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from dw6.state_manager import WorkflowManager, WorkflowState
from dw6.workflow.kernel import WorkflowKernel
from tests.tst import tfc, ter, tec, trc, tcn, tvte, tvtd, thp

class TestWorkflowManagerIntegration(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('dw6.state_manager.WorkflowState')
        self.mock_WorkflowState = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_failure_counter_and_rehearsal_transition(self):
        tfc.tfc(self)

    def test_engineer_to_researcher_transition(self):
        ter.ter(self)

    def test_engineer_to_coder_transition(self):
        tec.tec(self)

    def test_researcher_to_coder_transition(self):
        trc.trc(self)

    def test_create_new_requirement_json(self):
        tcn.tcn(self)

    def test_validator_to_engineer_transition(self):
        tvte.tvte(self)

    def test_validator_to_deployer_transition(self):
        tvtd.tvtd(self)

    def test_high_priority_event_insertion(self):
        thp.thp(self)

if __name__ == '__main__':
    unittest.main()
