import concurrent.futures
import threading
import functools
import time
try:
    import Queue as queue
except ImportError:
    import queue


class Switch:
    def __init__(self):
        self.on()

    def on(self):
        self.state = True

    def off(self):
        self.state = False

    def toggle(self):
        self.state = not self.state

    def __bool__(self):
        return self.state

    def __str__(self):
        state_string = "on" if self.state else "off"
        return "Switch: (%s)" % state_string


def threaded_generator(n_jobs=1, queue_size=0, timeout=0.1, stopper=None, stopper_timeout=0.1):
    def threaded_genrator_decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            result_queue = queue.Queue(maxsize=queue_size)
            keep_on_running = Switch()

            def do_work():
                try:
                    generator = iter(f(*args, **kwargs))
                except TypeError:
                    raise TypeError("function must be a generator or return an iterable")

                while keep_on_running:
                    try:
                        result = next(generator)
                        result_queue.put(result)
                    except StopIteration:
                        break

            workers = [threading.Thread(target=do_work) for _ in range(n_jobs)]

            try:
                if stop_when is not None:
                    def watch():
                        while not stopper() and keep_on_running:
                            time.sleep(stopper_timeout)
                        keep_on_running.off()
                    watcher_thread = threading.Thread(target=watch)
                    watcher_thread.daemon = True
                    watcher_thread.start()

                for worker in workers:
                    worker.daemon = True
                    worker.start()

                while any(w.is_alive() for w in workers) or not result_queue.empty():
                    try:
                        yield result_queue.get(timeout=timeout)
                    except queue.Empty:
                        pass
            finally:
                keep_on_running.off()
        return decorated
    return threaded_genrator_decorator
