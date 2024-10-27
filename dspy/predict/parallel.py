import threading

from typing import Tuple, List, Any

from ..primitives.example import Example
from ..utils.parallelizer import ParallelExecutor


class Parallel:
    def __init__(
        self,
        num_threads: int = 32,
        max_errors: int = 10,
        return_failed_examples: bool = False,
        provide_traceback: bool = False,
    ):
        super().__init__()
        self.num_threads = num_threads
        self.max_errors = max_errors
        self.return_failed_examples = return_failed_examples
        self.provide_traceback = provide_traceback

        self.error_count = 0
        self.error_lock = threading.Lock()
        self.cancel_jobs = threading.Event()
        self.failed_examples = []
        self.exceptions = []


    def forward(self, exec_pairs: List[Tuple[Any, Example]], num_threads: int = None) -> List[Any]:
        num_threads = num_threads if num_threads is not None else self.num_threads

        executor = ParallelExecutor(
            num_threads=num_threads,
            display_progress=True,
            max_errors=self.max_errors,
            provide_traceback=self.provide_traceback,
        )

        def process_pair(pair):
            module, example = pair

            result = module(**example.inputs())
            return result

        # Execute the processing function over the execution pairs
        results = executor.execute(process_pair, exec_pairs)

        if self.return_failed_examples:
            return results, self.failed_examples, self.exceptions
        else:
            return results


    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.forward(*args, **kwargs)