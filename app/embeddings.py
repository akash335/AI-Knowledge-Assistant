from functools import lru_cache

import numpy as np
from fastembed import TextEmbedding

from app.config import EMBEDDING_MODEL


class FastEmbedWrapper:

    def __init__(self):
        self.model = TextEmbedding(
            model_name=EMBEDDING_MODEL
        )

    def embed_documents(self, texts):
        vectors = list(
            self.model.embed(
                [f"passage: {text}" for text in texts]
            )
        )

        return [
            self._normalize(vector)
            for vector in vectors
        ]

    def embed_query(self, text):
        vector = list(
            self.model.embed(
                [f"query: {text}"]
            )
        )[0]

        return self._normalize(vector)

    @staticmethod
    def _normalize(vector):
        vector = np.asarray(
            vector,
            dtype=np.float32
        )

        norm = np.linalg.norm(vector)

        if norm == 0:
            return vector.tolist()

        return (vector / norm).tolist()


@lru_cache(maxsize=1)
def get_embeddings():
    return FastEmbedWrapper()
