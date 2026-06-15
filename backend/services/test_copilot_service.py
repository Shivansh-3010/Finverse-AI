from services.copilot_service import (
    CopilotService,
)

result = (
    CopilotService.analyze(
        "RELIANCE"
    )
)

print(result)