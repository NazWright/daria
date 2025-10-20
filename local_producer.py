import os
import json
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import boto3

MAX_RECORDS_PER_CALL = 500
MAX_REQUEST_BYTES = 5 * 1024 * 1024


def partition_key_for_row(row: dict) -> str:
    key_src = str(row.get("merchant", "")) + str(row.get("timestamp", ""))
    return hashlib.sha1(key_src.encode()).hexdigest()


def batch_records(rows):
    batch = []
    batch_bytes = 0
    for row in rows:
        payload = json.dumps(row, default=str).encode("utf-8")
        record_size = len(payload)
        if record_size > (1 * 1024 * 1024):
            continue
        entry = {"Data": payload, "PartitionKey": partition_key_for_row(row)}
        if len(batch) + 1 > MAX_RECORDS_PER_CALL or (batch_bytes + record_size) > MAX_REQUEST_BYTES:
            yield batch
            batch = [entry]
            batch_bytes = record_size
        else:
            batch.append(entry)
            batch_bytes += record_size
    if batch:
        yield batch


def make_kinesis_client(region: str, endpoint_url: str = None):
    kwargs = {"region_name": region}
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
    return boto3.client("kinesis", **kwargs)


def send_batch(client, stream_name: str, batch, retries: int = 3):
    for attempt in range(1, retries + 1):
        resp = client.put_records(Records=batch, StreamName=stream_name)
        failed = resp.get("FailedRecordCount", 0)
        if failed == 0:
            return resp
        retry_records = []
        for i, rec in enumerate(resp["Records"]):
            if "ErrorCode" in rec:
                retry_records.append(batch[i])
        if not retry_records:
            return resp
        batch = retry_records
        time.sleep(0.5 * (2 ** (attempt - 1)))
    return resp


def stream_rows(rows, stream_name, region="us-east-1", endpoint=None, workers=4):
    client = make_kinesis_client(region, endpoint)
    batches = list(batch_records(rows))
    print(f"Prepared {len(batches)} batches")
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(send_batch, client, stream_name, b) for b in batches]
        for f in as_completed(futures):
            try:
                r = f.result()
            except Exception as e:
                print("Batch failed:", e)


if __name__ == "__main__":
    # Simple demo dataset
    demo_rows = [{"id": i, "merchant": "acme", "timestamp": time.time(), "amount": i * 1.23} for i in range(1000)]
    stream = os.environ.get("LOCAL_KINESIS_STREAM", "fraud-stream")
    endpoint = os.environ.get("KINESIS_ENDPOINT")
    region = os.environ.get("AWS_REGION", "us-east-1")
    stream_rows(demo_rows, stream, region=region, endpoint=endpoint, workers=4)
