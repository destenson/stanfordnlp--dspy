from abc import ABC, abstractmethod


class BaseLM(ABC):
    def __init__(self, model, model_type='chat', temperature=0.0, cache=True, **kwargs):
        self.model = model
        self.model_type = model_type
        self.cache = cache
        self.kwargs = dict(temperature=temperature, **kwargs)
        self.history = []
    
    @abstractmethod
    def __call__(self, prompt=None, messages=None, **kwargs):
        pass
    
    def inspect_history(self, n: int = 1):
        _inspect_history(self, n)


def _green(text: str, end: str = "\n"):
    return "\x1b[32m" + str(text).lstrip() + "\x1b[0m" + end

def _red(text: str, end: str = "\n"):
    return "\x1b[31m" + str(text) + "\x1b[0m" + end

def _inspect_history(lm, n: int = 1):
    """Prints the last n prompts and their completions."""

    for item in reversed(lm.history[-n:]):
        messages = item["messages"] or [{"role": "user", "content": item['prompt']}]
        outputs = item["outputs"]

        print("\n\n\n")
        for msg in messages:
            print(_red(f"{msg['role'].capitalize()} message:"))
            if isinstance(msg['content'], str):
                print(msg['content'].strip())
            else:
                if isinstance(msg['content'], list):
                    for c in msg['content']:
                        if c["type"] == "text":
                            print(c["text"].strip())
                        elif c["type"] == "image_url":
                            print("<IMAGE URL>\n")
            print("\n")

        print(_red("Response:"))
        print(_green(outputs[0].strip()))

        if len(outputs) > 1:
            choices_text = f" \t (and {len(outputs)-1} other completions)"
            print(_red(choices_text, end=""))
        
    print("\n\n\n")