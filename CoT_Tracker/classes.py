import asyncio
import json
import random

import urllib.request
import urllib.error

import logging

import CoT_Tracker


class Worker:  # pylint: disable=too-few-public-methods

    """Meta class for all other Worker Classes."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(CoT_Tracker.constants.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(CoT_Tracker.constants.LOG_LEVEL)
        _console_handler.setFormatter(CoT_Tracker.constants.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False
    logging.getLogger("asyncio").setLevel(CoT_Tracker.constants.LOG_LEVEL)

    def __init__(self, event_queue: asyncio.Queue) -> None:
        self.event_queue: asyncio.Queue = event_queue

    async def run(self) -> None:
        """Placeholder Run Method for this Class."""
        self._logger.warning("Overwrite this method!")


class TrackerReceiverWorker(Worker):

    def __init__(self, event_queue: asyncio.Queue,
                 cot_stale: int = None, poll_interval: int = None):
        super().__init__(event_queue)
        self.cot_stale: int = int(cot_stale or
                                  CoT_Tracker.constants.DEFAULT_INTERVAL)
        self.poll_interval: int = int(poll_interval or
                                      CoT_Tracker.constants.DEFAULT_INTERVAL)
        self.accountID = ""
        self.sessionID = ""

    async def handle_message(self, devices: list) -> None:
        self._logger.info("handling message")
        if not devices:
            self._logger.warning("Empty device list")
            return None
        n = 1
        for device in devices:
            event = CoT_Tracker.functions.json_to_cot(device, self.cot_stale)
            await self.event_queue.put(event)
            self._logger.info("Added "+str(n)+" of "+str(len(devices))+" devices to que")
            n = n+1

    async def _get_devices(self):
        self._logger.info("Getting devices")
        try:
            r = urllib.request.urlopen(
                'http://mobile.trackserver.co.uk/api/api/MobileApp/GetDeviceData?SessionID=' + self.sessionID + '&AccountID=' + str(
                    self.accountID) + '&PullAll=true')
        except urllib.error.HTTPError:
            self.sessionID, self.accountID = CoT_Tracker.functions.login()
            r = urllib.request.urlopen(
                'http://mobile.trackserver.co.uk/api/api/MobileApp/GetDeviceData?SessionID=' + self.sessionID + '&AccountID=' + str(
                    self.accountID) + '&PullAll=true')
        json_data = r.read()
        parsed_json = (json.loads(json_data))
        devices = parsed_json["Devices"]
        self._logger.info("Retrieved %s devices", len(devices))
        await self.handle_message(devices)

    async def run(self):
        """Runs this Thread, Reads from Pollers."""
        self._logger.info("Running TrackerReceiverWorker")
        while 1:
            self._logger.info("Logging in")
            self.sessionID, self.accountID = CoT_Tracker.functions.login()
            self._logger.info("Retreived sessinID=" + str(self.sessionID) + " and accountID=" + str(self.accountID))
            await self._get_devices()
            await asyncio.sleep(self.poll_interval)


class EventTransmitter(Worker):  # pylint: disable=too-few-public-methods

    """
    EventWorker handles getting Cursor on Target Events from a queue, and
    passing them off to a transport worker.

    """

    def __init__(self, tx_queue: asyncio.Queue, writer) -> None:
        super().__init__(tx_queue)
        self.writer = writer

    async def run(self):
        """Runs this Thread, reads in Message Queue & sends out CoT."""
        self._logger.info('Running EventTransmitter')
        while 1:
            tx_event = await self.event_queue.get()
            self._logger.info('Got event from tx_queue')
            if not tx_event:
                continue

            if isinstance(tx_event, CoT_Tracker.Event):
                _event = tx_event.generate_cot()
            else:
                _event = tx_event
            print(str(_event))
            self._logger.info("Sending event to server "+CoT_Tracker.DEFAULT_COT_IP+":"+str(CoT_Tracker.DEFAULT_COT_PORT))
            self.writer.write(_event)
            self._logger.info("Event send to server")
            await self.writer.drain()

            await asyncio.sleep(CoT_Tracker.DEFAULT_SLEEP * random.random())


class EventReceiver(Worker):  # pylint: disable=too-few-public-methods

    def __init__(self, rx_queue: asyncio.Queue, reader) -> None:
        super().__init__(rx_queue)
        self.reader = reader

    async def run(self):
        self._logger.info('Running EventReceiver')
        while 1:
            rx_event = await self.event_queue.get()
