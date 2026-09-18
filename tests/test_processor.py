import pytest
from data_validator.processor import AsyncBatchProcessor


@pytest.mark.asyncio
async def test_batch_processor_handles_valid_and_invalid():
    sample_dataset = [
        {
            "id": "usr_101",
            "name": "  ada lovelace  ",
            "email": "ada@computing.org",
            "age": 36,
            "signup_date": "2026-03-01T10:00:00Z",
            "balance": 250.75,
        },
        {
            "id": "usr_102",
            "name": "Bob Minor",
            "email": "bob@domain.com",
            "age": 16,  # Under 18 constraint
            "signup_date": "2026-03-02T12:00:00Z",
            "balance": 10.0,
        },
        {
            "id": "usr_103",
            "name": "Charles Babbage",
            "email": "not-a-valid-email",  # Invalid EmailStr
            "age": 79,
            "signup_date": "2026-03-03T15:30:00Z",
            "balance": 0.0,
        },
    ]

    processor = AsyncBatchProcessor(max_concurrency=4)
    summary = await processor.process_batch(sample_dataset)

    # Invariants verification
    assert summary.total_processed == 3
    assert len(summary.successful_records) == 1
    assert len(summary.failed_records) == 2

    # Verify custom normalization validator
    valid_record = summary.successful_records[0]
    assert valid_record.name == "Ada Lovelace"
    assert valid_record.id == "usr_101"

    # Verify failed record IDs
    failed_ids = [item["id"] for item in summary.failed_records]
    assert "usr_102" in failed_ids
    assert "usr_103" in failed_ids