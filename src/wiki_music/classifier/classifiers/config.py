BATCH_SIZE = 50
DEFAULT_SYSTEM_PROMPT = """You are classifying Wikipedia articles based off the first sentence
of the article (the summary). You are determining whether or not a given article describes a 
piece of music, a musician, a musical, or an opera. Include disambiguation pages (those with "may
refer to") if at least of the elements listed is a musician or points towards a musician.""" 

DEFAULT_USER_PROMPT = """For each of the summaries below, classify if it describes a piece of music.
Return a list that has the same number of elements as the """
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
                },
                "minItems": 10,
                "maxItems": 10
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