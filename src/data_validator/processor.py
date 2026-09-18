import asyncio
import time
from typing import Any
from pydantic import ValidationError
from data_validator.models import UserRecordInput, ValidationSummary


class AsyncBatchProcessor:
    def __init__(self, max_concurrency: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def _validate_single_record(self, raw_record: dict[str, Any]) -> tuple[bool, Any]:
        async with self.semaphore:
            # Yield to the event loop simulating non-blocking task handling
            await asyncio.sleep(0.001)
            try:
                validated = UserRecordInput(**raw_record)
                return True, validated
            except ValidationError as err:
                record_id = str(raw_record.get("id", "UNKNOWN"))
                # Extract first human-readable validation error message
                error_msg = err.errors()[0]["msg"]
                return False, {"id": record_id, "error": error_msg}

    async def process_batch(self, raw_records: list[dict[str, Any]]) -> ValidationSummary:
        start_time = time.perf_counter()
        
        # Schedule all records concurrently within bounded semaphore limits
        tasks = [self._validate_single_record(record) for record in raw_records]
        results = await asyncio.gather(*tasks)

        summary = ValidationSummary()
        summary.total_processed = len(raw_records)

        for is_valid, payload in results:
            if is_valid:
                summary.successful_records.append(payload)
            else:
                summary.failed_records.append(payload)

        summary.duration_seconds = round(time.perf_counter() - start_time, 4)
        return summary