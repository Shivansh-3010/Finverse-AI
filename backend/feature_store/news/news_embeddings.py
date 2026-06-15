import chromadb


class NewsEmbeddings:

    def __init__(self):

        self.client = (
            chromadb.PersistentClient(
                path="../database/chromadb"
            )
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="news_embeddings"
            )
        )

    def add_news(
        self,
        news_id: str,
        headline: str,
        metadata: dict
    ):

        self.collection.add(
            ids=[
                news_id
            ],
            documents=[
                headline
            ],
            metadatas=[
                metadata
            ]
        )

    def search(
        self,
        query: str,
        limit: int = 5
    ):

        return self.collection.query(
            query_texts=[
                query
            ],
            n_results=limit
        )