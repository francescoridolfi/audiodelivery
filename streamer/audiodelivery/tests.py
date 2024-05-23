from django.test import TestCase

from audiodelivery.models.chunk import AudioChunk

from audiodelivery.utils.time import convert_to_millis, convert_from_millis

import logging

logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.DEBUG)

class AudioChunkTestCase(TestCase):

    def setUp(self) -> None:
        AudioChunk.objects.create(
            order=1,
            start_time="T00:00:00.0",
            end_time="T08:12:40.999000" # Expected: ((8*60 + 12)*60 + 40)*1000 + 999 = 29560999
        )
        AudioChunk.objects.create(
            order=2,
            start_time="T08:12:41.0",
            end_time="T09:12:40.999000"
        )

    def test_retrieve_all_chunks(self):
        for chunk in AudioChunk.objects.all():
            logger.debug(
                f"{chunk} -> [start time: {convert_to_millis(chunk.start_time)}, end time: {convert_to_millis(chunk.end_time)}]"
            )
    
    def test_millis(self):
        chunk = AudioChunk.objects.get(order=1)

        self.assertEqual(convert_to_millis(chunk.end_time), int(((8*60 + 12)*60 + 40)*1000 + 999), "Chunk n1 did not return the expected value")

        self.assertEqual(convert_from_millis(29560999), "T08:12:40.999", "Converting from millis failed due to invalid output")

        self.assertEqual(convert_from_millis(0), "T00:00:00.0", "Converting from millis failed due to invalid output")
