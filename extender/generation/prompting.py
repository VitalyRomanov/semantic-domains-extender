from copy import copy


class PromptBuilder:
    def __init__(self):
        self.prompt = ""

    def __add__(self, extension: str):
        self.prompt += extension
        return self

    def estimate_tokens(self, string):
        return len(string.split()) * 2.5

    def truncate(self, max_length, split_on: str = "lines"):
        
        assert split_on == "lines"

        num_tokens = 0
        truncated_lines = []
        for line in reversed(self.prompt.split("\n")):
            line_tokens = self.estimate_tokens(line)
            if line_tokens + num_tokens > max_length:
                break

            truncated_lines.append(line)
            num_tokens += line_tokens

        truncated_prompt = "\n".join(reversed(truncated_lines))
        return self.__class__() + truncated_prompt
    
    def __repr__(self):
        return copy(self.prompt)
    
    def copy(self):
        return self.__class__() + self.prompt
