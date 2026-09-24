# from engineering_team.knowledge.ingestion import process_document
from engineering_team.knowledge.ingestion import process_document
from engineering_team.knowledge.ingestion import process_documents
file_path = "ExampleTech_Sample_Leave_Policy.docx"

chunks = process_document(file_path)

print(f"Number of chunks: {len(chunks)}")

for chunk in chunks:

    print("\n-----------------------------")
    print(f"Source: {chunk['source']}")
    print(f"Chunk ID: {chunk['chunk_id']}")
    print("-----------------------------")

    print(chunk["text"][:500])