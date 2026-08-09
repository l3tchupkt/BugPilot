from kosong.tooling import CallableTool2, ToolReturnValue
from pydantic import BaseModel, Field

from bugpilot.soul.agent import Runtime

class GenerateReportParams(BaseModel):
    title: str = Field(description="A concise title for the security finding.")
    severity: str = Field(description="The severity of the finding (e.g. Critical, High, Medium, Low).")
    cvss_score: float | None = Field(description="The CVSS score if applicable.", default=None)
    description: str = Field(description="A detailed technical description of the vulnerability.")
    impact: str = Field(description="The potential impact of the vulnerability.")
    remediation: str = Field(description="Recommended steps to fix the issue.")
    proof_of_concept: str = Field(description="Step-by-step instructions or code to reproduce the issue.")

class GenerateReportTool(CallableTool2[GenerateReportParams]):
    name = "generate_report"
    description = "Generate a structured security report for a confirmed finding. You MUST call this to finish your task."
    params = GenerateReportParams

    def __init__(self, runtime: Runtime):
        super().__init__()
        self._runtime = runtime

    async def __call__(self, params: GenerateReportParams) -> ToolReturnValue:
        # Just format the report beautifully so it gets captured in the agent's final output or saved to a file later.
        output = (
            f"# {params.title}\n\n"
            f"**Severity:** {params.severity}\n"
            f"**CVSS Score:** {params.cvss_score or 'N/A'}\n\n"
            f"## Description\n{params.description}\n\n"
            f"## Impact\n{params.impact}\n\n"
            f"## Proof of Concept\n{params.proof_of_concept}\n\n"
            f"## Remediation\n{params.remediation}\n"
        )
        
        # Save a copy to artifacts? For now returning to context is fine, parent will see it.
        return output
