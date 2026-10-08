"""Wave 23 Lane B — EBU-TT Live WebSocket carriage smoke test (producer side).

Runs a real Twisted WebSocket server (the toolkit's BroadcastServerFactory +
TwistedWSPushProducer + WebsocketProducerCarriage chain) on 127.0.0.1:9000 and
pushes a finite run of EBU-TT Live Part 3 documents, one per second, per
EBU Tech 3370s1 (WebSocket carriage). Uses only the toolkit's own classes.
"""
import logging
import sys
from itertools import cycle

from twisted.internet import task, reactor

from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.documents import EBUTT3DocumentSequence
from ebu_tt_live.node import SimpleProducer
from ebu_tt_live.twisted import (
    BroadcastServerFactory,
    BroadcastServerProtocol,
    TwistedWSPushProducer,
)
from ebu_tt_live.carriage.websocket import WebsocketProducerCarriage
from ebu_tt_live.adapters.node_carriage import ProducerNodeCarriageAdapter

logging.basicConfig(level=logging.WARNING)

SEQUENCE_ID = "SmokeTest1"
PORT = 9000


class BytesEncodingProducerCarriage(WebsocketProducerCarriage):
    """Harness workaround for a genuine upstream bug: with autobahn>=20.x,
    WebSocket payloads must be bytes, but the toolkit hands str to
    sendMessage(), which now asserts. Encode here; the toolkit itself is
    untouched."""

    def emit_data(self, data, sequence_identifier="default", delay=None, **kwargs):
        if isinstance(data, str):
            data = data.encode("utf-8")
        super().emit_data(
            data, sequence_identifier=sequence_identifier, delay=delay, **kwargs
        )

BLOCKS = [
    "First live caption document over WebSocket.",
    "Second document, same sequence identifier.",
    "Third document. Sequence numbers must increment.",
    "Fourth and final document of the smoke run.",
]


def main():
    reference_clock = LocalMachineClock()
    reference_clock.clock_mode = "local"

    document_sequence = EBUTT3DocumentSequence(
        sequence_identifier=SEQUENCE_ID,
        lang="en-GB",
        reference_clock=reference_clock,
    )

    prod_impl = BytesEncodingProducerCarriage()
    prod_impl.sequence_identifier = SEQUENCE_ID

    simple_producer = SimpleProducer(
        node_id="smoke-producer",
        producer_carriage=None,
        document_sequence=document_sequence,
        input_blocks=cycle(BLOCKS),
    )
    ProducerNodeCarriageAdapter(
        producer_carriage=prod_impl,
        producer_node=simple_producer,
    )

    twisted_producer = TwistedWSPushProducer(custom_producer=prod_impl)
    factory = BroadcastServerFactory(
        url="ws://127.0.0.1:%d" % PORT,
        producer=twisted_producer,
    )
    factory.protocol = BroadcastServerProtocol
    factory.listen()

    looping = task.LoopingCall(simple_producer.process_document)
    looping.start(1.0)

    # Keep the server up for a generous window so the consumer can connect.
    reactor.callLater(45, reactor.stop)
    reactor.run()
    print("PRODUCER_DONE blocks=%d" % len(BLOCKS), flush=True)


if __name__ == "__main__":
    sys.exit(main())
