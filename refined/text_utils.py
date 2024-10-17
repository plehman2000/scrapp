from langchain_text_splitters import RecursiveCharacterTextSplitter 


def chunk_text(text, max_tokens=300, overlap_ratio=0.50):
    splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=max_tokens,
        chunk_overlap=int(max_tokens * overlap_ratio),
        length_function=len,
        is_separator_regex=False,
        separators=['.', '\n']
    )
    # Split the content into chunks
    # chunks = splitter.chunks(content)

    chunks = splitter.split_text(text)

    return chunks
