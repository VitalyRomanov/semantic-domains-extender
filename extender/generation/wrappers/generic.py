from typing import Any, Optional, Union

from extender.generation.prompting import PromptBuilder


class GeneratorWrapper:
    def __init__(self, llm: Any, initial_prompt: Optional[Union[str, PromptBuilder]] = None):
        if initial_prompt is None:
            initial_prompt = ""
        self.llm = llm
        self.append(initial_prompt)

    def prompt_as_string(self, prompt: Union[str, PromptBuilder]):
        if isinstance(prompt, str):
            return prompt
        elif isinstance(prompt, PromptBuilder):
            return repr(prompt)
        else:
            raise TypeError(f"Prompt must be a string or a PromptBuilder")

    def append(self, text: Union[str, PromptBuilder]):
        self.llm += self.prompt_as_string(text)

    def gen_append(self, **kwargs):
        raise NotImplementedError("Subclasses must implement gen_append")
        existing = str(self.llm)
        self.llm += gen(**kwargs)
        generated = str(self.llm)[len(existing):]
        return generated