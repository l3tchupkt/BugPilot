from typing import Literal

from kosong.tooling import CallableTool2, ToolReturnValue
from pydantic import BaseModel, Field

from bugpilot.soul.agent import Runtime

class SubmitTriageVerdictParams(BaseModel):
    verdict: Literal["confirmed", "false_positive", "insufficient_evidence", "duplicate", "out_of_scope"] = Field(
        description="The final verdict for the candidate finding."
    )
    confidence: Literal["low", "medium", "high"] = Field(
        description="Your confidence in this verdict."
    )
    reasoning: str = Field(
        description="Detailed reasoning for why this verdict was chosen."
    )
    evidence_reviewed: list[str] = Field(
        description="List of specific files, logs, or PoCs you reviewed to reach this conclusion."
    )

class SubmitTriageVerdictTool(CallableTool2[SubmitTriageVerdictParams]):
    name = "submit_triage_verdict"
    description = "Submit your final verdict for a candidate finding. You MUST call this to finish your task."
    params = SubmitTriageVerdictParams

    def __init__(self, runtime: Runtime):
        super().__init__()
        self._runtime = runtime

    async def __call__(self, params: SubmitTriageVerdictParams) -> ToolReturnValue:
        # For now, just print it out and format it nicely for the parent agent to read.
        output = (
            f"**Triage Verdict:** {params.verdict.upper()}\n"
            f"**Confidence:** {params.confidence.upper()}\n\n"
            f"**Reasoning:**\n{params.reasoning}\n\n"
            f"**Evidence Reviewed:**\n" + "\n".join(f"- {e}" for e in params.evidence_reviewed)
        )
        return output
