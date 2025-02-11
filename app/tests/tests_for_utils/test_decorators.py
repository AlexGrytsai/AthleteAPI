import asyncio
import unittest
from unittest.mock import patch

from app.utils.decorators import (
    async_timer_of_execution,
    sync_timer_of_execution,
)


class TestTimerDecorators(unittest.TestCase):
    @patch("app.utils.decorators.logger")
    def test_sync_timer_of_execution(self, mock_logger):
        @sync_timer_of_execution
        def sample_function():
            return "Hello"

        result = sample_function()

        self.assertEqual(result, "Hello")
        mock_logger.info.assert_called_once()
        self.assertIn(
            "Execution time for 'sample_function'",
            mock_logger.info.call_args[0][0],
        )

    @patch("app.utils.decorators.logger")
    def test_async_timer_of_execution(self, mock_logger):
        @async_timer_of_execution
        async def sample_async_function():
            await asyncio.sleep(0.1)
            return "Async Hello"

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(sample_async_function())

        self.assertEqual(result, "Async Hello")
        mock_logger.info.assert_called_once()
        self.assertIn(
            "Execution time for 'sample_async_function'",
            mock_logger.info.call_args[0][0],
        )
