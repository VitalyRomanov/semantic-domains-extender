from guidance import gen

from extender.generation.wrappers.generic import GeneratorWrapper


class GuidanceGeneratorWrapper(GeneratorWrapper):
    def gen_append(self, **kwargs):
        existing = str(self.llm)
        self.llm += gen(**kwargs)
        generated = str(self.llm)[len(existing):]
        return generated