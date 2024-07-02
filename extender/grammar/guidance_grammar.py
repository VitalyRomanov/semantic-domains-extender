import guidance
from guidance import select, with_temperature

from extender.grammar.parser import GrammarParser


@guidance(stateless=True)  # type: ignore
def select_with_temperature(lm, options, temperature=0.0):
    return lm + with_temperature(select(options), temperature=temperature)


class GuidanceGrammar:
    def __init__(self, grammar: str) -> None:
        parser = GrammarParser(grammar)
        self._non_terminals, self._terminals = parser.parse(grammar)
        self._terminals["sep"] = [' ']
        self._terminals["eos"] = ['.', '?', '!']
        
    @guidance(stateless=True)  # type: ignore
    def select_terminal(lm, self, rule, temperature=0.0, add_leading_sep=True):
        return (  # TODO select seems to be broken
            lm +   # type: ignore
            (self.select_terminal("sep", temperature=temperature, add_leading_sep=False) if add_leading_sep else "") + 
            select_with_temperature(self._terminals[rule], temperature=temperature)  # type: ignore  
        )
    
    @guidance()  # type: ignore
    def combine(lm, self, grammars, temperature=0.0):
        for grammar in grammars:
            lm += self.construct_recursively(grammar, temperature=temperature)
        return lm
    
    @guidance()  # type: ignore
    def construct_recursively(lm, self, rule, temperature=0.0):
        if rule in self._terminals:
            lm += self.select_terminal(rule, temperature=temperature)
        elif rule in self._non_terminals:
            options = self._non_terminals[rule]
            lm += select_with_temperature(  # type: ignore
                [self.combine(option, temperature=temperature) for option in options], 
                temperature=temperature
            )
        else:
            raise ValueError(f"Unrecognized grammar: {rule}")
        return lm
    
    @guidance()  # type: ignore
    def __call__(lm, self, temperature=0.0):
        assert "TOP" in self._non_terminals
        return (
            lm + self.construct_recursively("TOP", temperature=temperature) + 
            self.select_terminal("eos", temperature=temperature, add_leading_sep=False)
        )
