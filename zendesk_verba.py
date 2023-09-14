import itertools

import dlt
from weaviate.util import generate_uuid5
from dlt.destinations.weaviate import weaviate_adapter

from zendesk import zendesk_support


def to_verba_document(ticket):
    # The document id is the ticket id.
    # dlt will use this to generate a UUID for the document in Weaviate.
    return {
        "doc_id": ticket["id"],
        "doc_name": ticket["subject"],
        "doc_type": "Zendesk ticket",
        "doc_link": ticket["url"],
        "text": ticket["description"],
    }


def to_verba_chunk(ticket):
    # We link the chunk to the document by using the document (ticket) id.
    return {
        "chunk_id": 0,
        "doc_name": ticket["subject"],
        "doc_type": "Zendesk ticket",
        "doc_uuid": generate_uuid5(ticket["id"], "Document"),
        "text": ticket["description"],
    }


def main():
    pipeline = dlt.pipeline(
        pipeline_name="zendesk_verba",
        destination="weaviate",
    )

    # Zendesk Support has data tickets, users, groups, etc.
    zendesk_source = zendesk_support(load_all=False)

    # Here we get a dlt resource containing only the tickets
    tickets = zendesk_source.tickets

    # Split the tickets into two streams
    tickets1, tickets2 = itertools.tee(tickets, 2)

    @dlt.resource(primary_key="doc_id", write_disposition="merge")
    def document():
        # Map over the tickets and convert them to Verba documents
        # primary_key is the field that will be used to generate
        # a UUID for the document in Weaviate.
        yield from weaviate_adapter(
            map(to_verba_document, tickets1),
            vectorize="text",
        )

    @dlt.resource
    def chunk():
        yield from weaviate_adapter(
            map(to_verba_chunk, tickets2),
            vectorize="text",
        )

    info = pipeline.run([document, chunk])

    return info


if __name__ == "__main__":
    load_info = main()
    print(load_info)
