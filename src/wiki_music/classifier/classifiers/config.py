BATCH_SIZE = 50
DEFAULT_SYSTEM_PROMPT = "You are classifying Wikipedia article summaries ..." #TODO: complete initial prompt
DEFAULT_USER_PROMPT = "Classify if each summary below describes a piece of music ..." #TODO: complete initial prompt
MODEL = "gpt-4o-mini"
FUNCTION_SCHEMA = {
    "name": "classify_summaries",
    "description": "Classify if Wikipedia summaries describe music",
    "parameters": {
        "type": "object",
        "properties": {
            "classifications": {
                "type": "array",
                "items": {
                    "type": "boolean"
                }
            }
        },
        "required": ["classifications"],
        "additionalProperties": False,
    }
}
TOOLS_SCHEMA = [{
    "type": "function",
    "function": {
        **FUNCTION_SCHEMA,
        "strict":True
    }
}]