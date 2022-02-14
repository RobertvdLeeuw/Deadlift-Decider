from threading import Thread, Lock


class ThreadManager:
	_threads = list()
	_running = False

	def __init__(self, threadLimit: int, dataQueue: list, function, lock: Lock):
		self._threadLimit = threadLimit
		self._dataQueue = dataQueue
		self._function = function
		self._lock = lock

	def _AddThread(self, func, args: tuple) -> bool:
		if len(self._threads) >= self._threadLimit:
			return False

		newThread = Thread(target=func, args=args)
		newThread.daemon = True
		newThread.start()

		self._threads.append(newThread)
		return True

	def _ManageThreads(self) -> bool:
		while self._running:
			self._threads = [t for t in self._threads if t.is_alive()]
			# print(f"WORK LEFT: {len(self._dataQueue)} cycles. Currently {len(self._threads)} active.")

			while True:
				if not self._dataQueue:
					self.Stop()
					break

				args = self._dataQueue[0]  # To mimic 'peeking'.
				if not isinstance(args, list):
					args = [args]

				args.insert(0, self._lock)

				filled = not self._AddThread(self._function, tuple(args))  # Returns false when a thread couldn't be added (because the limit hass been reached).

				if filled:
					break

				self._dataQueue.pop(0)  # Takes the args out the of the queue if they got processed.

		while True:  # Waiting for the last ones to finish.
			self._threads = [t for t in self._threads if t.is_alive()]

			if not self._threads:
				break

		return True

	def Start(self) -> bool:
		self._running = True

		return self._ManageThreads()

	def Stop(self):
		self._running = False
