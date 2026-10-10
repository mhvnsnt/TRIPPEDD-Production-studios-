"""Wave 23 Lane B — EBU-TT Live WebSocket carriage smoke test (consumer side).

Connects to ws://localhost:9000/<sequence>/subscribe using the toolkit's
BroadcastClientFactory + TwistedWSConsumer + WebsocketConsumerCarriage chain,
records every EBU-TT Live document received (sequence identifier, sequence
number, payload text), and writes a JSON verdict to received.json.
"""
import json
import logging
import sys

from twisted.internet import reactor

from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.node import SimpleConsumer
from ebu_tt_live.twisted import TwistedWSConsumer, BroadcastClientFactory, BroadcastClientProtocol
from ebu_tt_live.carriage.websocket import WebsocketConsumerCarriage
from ebu_tt_live.adapters.node_carriage import ConsumerNodeCarriageAdapter

logging.basicConfig(level=logging.INFO)

SEQUENCE_ID = "SmokeTest1"
URL = "ws://localhost:9000/%s/subscribe" % SEQUENCE_ID
EXPECT = 4

received = []
received_raw = []


def main():
    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = "local"

    consumer_impl = WebsocketConsumerCarriage()

    # Harness counterpart of the producer-side bytes workaround: the toolkit's
    # XML->document data adapter expects str (six.text_type).
    _orig_on_new_data = consumer_impl.on_new_data

    def _decoding_on_new_data(data, **kwargs):
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        # Stash the raw XML for the proof artifact before the adapter parses it.
        received_raw.append(data)
        return _orig_on_new_data(data, **kwargs)

    consumer_impl.on_new_data = _decoding_on_new_data
    simple_consumer = SimpleConsumer(
        node_id="smoke-consumer",
        reference_clock=reference_clock,
    )
    ConsumerNodeCarriageAdapter(
        consumer_node=simple_consumer,
        consumer_carriage=consumer_impl,
    )

    orig_process = simple_consumer.process_document

    def recording_process(document, **kwargs):
        raw = received_raw[-1] if received_raw else ""
        received.append(
            {
                "sequence_identifier": document.sequence_identifier,
                "sequence_number": document.sequence_number,
                "xml_bytes": len(raw.encode("utf-8")),
                "text_hint": raw[:200].replace("\n", " "),
            }
        )
        orig_process(document, **kwargs)
        if len(received) >= EXPECT:
            reactor.callLater(0.5, reactor.stop)

    simple_consumer.process_document = recording_process

    twisted_consumer = TwistedWSConsumer(custom_consumer=consumer_impl)
    factory = BroadcastClientFactory(url=URL, consumer=twisted_consumer)
    factory.protocol = BroadcastClientProtocol
    factory.connect()

    reactor.callLater(30, reactor.stop)  # hard timeout
    reactor.run()

    seq_ok = all(r["sequence_identifier"] == SEQUENCE_ID for r in received)
    nums = [r["sequence_number"] for r in received]
    nums_ok = nums == sorted(nums) and len(set(nums)) == len(nums) and len(nums) > 0

    verdict = {
        "received_count": len(received),
        "expected": EXPECT,
        "all_sequence_identifiers_match": seq_ok,
        "sequence_numbers": nums,
        "sequence_numbers_monotonic_unique": nums_ok,
        "pass": len(received) >= EXPECT and seq_ok and nums_ok,
        "documents": received,
    }
    with open("received.json", "w") as f:
        json.dump(verdict, f, indent=2)
    print("CONSUMER_DONE received=%d pass=%s" % (len(received), verdict["pass"]), flush=True)
    return 0 if verdict["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
