import asyncio
import logging

import CoT_Tracker


async def main():
	_logger = logging.getLogger(__name__)
	if not _logger.handlers:
		_logger.setLevel(CoT_Tracker.constants.LOG_LEVEL)
		_console_handler = logging.StreamHandler()
		_console_handler.setLevel(CoT_Tracker.constants.LOG_LEVEL)
		_console_handler.setFormatter(CoT_Tracker.constants.LOG_FORMAT)
		_logger.addHandler(_console_handler)
		_logger.propagate = False
	logging.getLogger("asyncio").setLevel(CoT_Tracker.constants.LOG_LEVEL)

	tx_queue: asyncio.Queue = asyncio.Queue()
	rx_queue: asyncio.Queue = asyncio.Queue()
	reader, writer = await asyncio.open_connection(CoT_Tracker.constants.DEFAULT_COT_IP, CoT_Tracker.constants.DEFAULT_COT_PORT)
	write_worker = CoT_Tracker.EventTransmitter(tx_queue, writer)
	read_worker = CoT_Tracker.EventReceiver(rx_queue, reader)
	message_worker = CoT_Tracker.classes.TrackerReceiverWorker(tx_queue)

	_logger.info('Sending Hello')
	await tx_queue.put(CoT_Tracker.hello_event())

	done, pending = await asyncio.wait(
		{message_worker.run(), read_worker.run(), write_worker.run()},
		return_when=asyncio.FIRST_COMPLETED)

	for task in done:
		print(f"Task completed: {task}")


if __name__ == '__main__':
	asyncio.run(main())
