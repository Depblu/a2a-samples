import asyncio
import base64
import logging
import os
import statistics
import time
from typing import Any, Dict, List
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    Message,
    MessageSendParams,
    Part,
    SendMessageRequest,
    SendMessageSuccessResponse,
    TextPart,
)

# --- Test Configuration ---
PAYLOAD_SIZES_KB = [1, 4, 16, 64]  # In Kilobytes
PAYLOAD_SIZES_BYTES = [s * 1024 for s in PAYLOAD_SIZES_KB]
NUM_ITERATIONS = 10  # Number of tests per payload size
REPORT_FILE = 'latency_report.md'


async def main() -> None:
    """
    Main function to run the latency test client.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    base_url = 'http://localhost:9999'
    all_results: Dict[int, Dict[str, Any]] = {}

    async with httpx.AsyncClient(timeout=60.0) as httpx_client:
        try:
            # --- Agent Card Resolution ---
            logger.info('Resolving agent card...')
            resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
            agent_card: AgentCard = await resolver.get_agent_card()
            logger.info(f'Successfully resolved agent card: {agent_card.name}')

            client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)
            logger.info('A2AClient initialized.')

        except Exception as e:
            logger.error(f'Failed to initialize A2A client: {e}', exc_info=True)
            return

        # --- Warm-up Phase ---
        logger.info('\n--- Performing warm-up runs to stabilize the system... ---')
        try:
            warmup_payload = base64.b64encode(os.urandom(1024)).decode('utf-8')
            warmup_params = MessageSendParams(
                message={
                    'role': 'user',
                    'parts': [{'kind': 'text', 'text': warmup_payload}],
                }
            )
            for i in range(5):  # 5 warm-up runs
                request = SendMessageRequest(id=str(uuid4()), params=warmup_params)
                await client.send_message(request)
                logger.info(f'  Warm-up run {i+1} complete.')
        except Exception as e:
            logger.warning(f'An error occurred during warm-up: {e}. Continuing with tests.')

        # --- Latency Test Execution ---
        logger.info('\n--- Starting formal latency tests... ---')
        for size_bytes in PAYLOAD_SIZES_BYTES:
            size_kb = size_bytes // 1024
            logger.info(f'\n--- Testing with payload size: {size_kb} KB ---')
            latencies_ms: List[float] = []

            # Generate a single payload for this size to reuse
            payload_data = base64.b64encode(os.urandom(size_bytes)).decode('utf-8')

            for i in range(NUM_ITERATIONS):
                try:
                    request_params = MessageSendParams(
                        message={
                            'role': 'user',
                            'parts': [{'kind': 'text', 'text': payload_data}],
                            'messageId': uuid4().hex,
                        }
                    )
                    request = SendMessageRequest(id=str(uuid4()), params=request_params)

                    start_time = time.monotonic()
                    response = await client.send_message(request)
                    end_time = time.monotonic()

                    # Validate response by accessing the nested structure
                    if (
                        response.root
                        and isinstance(response.root, SendMessageSuccessResponse)
                        and response.root.result
                        and isinstance(response.root.result, Message)
                        and response.root.result.parts
                        and len(response.root.result.parts) > 0
                        and isinstance(response.root.result.parts[0], Part)
                        and isinstance(response.root.result.parts[0].root, TextPart)
                        and response.root.result.parts[0].root.text == payload_data
                    ):
                        latency_ms = (end_time - start_time) * 1000
                        latencies_ms.append(latency_ms)
                        logger.info(f'  Run {i+1:2d}/{NUM_ITERATIONS}: {latency_ms:8.2f} ms')
                    else:
                        logger.warning(f'  Run {i+1:2d}/{NUM_ITERATIONS}: Response validation failed.')

                except Exception as e:
                    logger.error(f'  Run {i+1:2d}/{NUM_ITERATIONS}: Request failed: {e}')

            # --- Statistical Calculation ---
            if latencies_ms:
                mean_latency = statistics.mean(latencies_ms)
                std_dev = statistics.stdev(latencies_ms) if len(latencies_ms) > 1 else 0.0
                all_results[size_kb] = {
                    'latencies': latencies_ms,
                    'mean': mean_latency,
                    'std_dev': std_dev,
                }
            else:
                 logger.warning(f"No successful runs for {size_kb} KB payload. Skipping stats.")


    # --- Report Generation ---
    generate_markdown_report(all_results)
    logger.info(f'\nTest complete. Report generated at: {REPORT_FILE}')


def generate_markdown_report(results: Dict[int, Dict[str, Any]]) -> None:
    """
    Generates a markdown report from the test results.
    """
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('# A2A Agent Latency Test Report\n\n')
        f.write(f'**Date:** {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'**Iterations per Payload:** {NUM_ITERATIONS}\n\n')

        # --- Summary Table ---
        f.write('## Summary\n\n')
        f.write('| Payload Size (KB) | Mean Latency (ms) | Std Deviation (ms) |\n')
        f.write('|-------------------|-------------------|--------------------|\n')
        for size_kb, data in sorted(results.items()):
            f.write(
                f'| {size_kb:<17} | {data["mean"]:>17.2f} | {data["std_dev"]:>18.2f} |\n'
            )
        f.write('\n')

        # --- Detailed Results ---
        f.write('## Detailed Results\n\n')
        for size_kb, data in sorted(results.items()):
            f.write(f'<details>\n')
            f.write(f'<summary><strong>{size_kb} KB Payload</strong></summary>\n\n')
            f.write('| Run # | Latency (ms) |\n')
            f.write('|-------|--------------|\n')
            for i, latency in enumerate(data['latencies']):
                f.write(f'| {i+1:<5} | {latency:>12.2f} |\n')
            f.write('\n</details>\n\n')


if __name__ == '__main__':
    asyncio.run(main())
