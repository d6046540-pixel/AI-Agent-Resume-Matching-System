from sentence_transformers import CrossEncoder



class Reranker:


    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base"
        )



    def rerank(
        self,
        query,
        documents,
        top_k=3
    ):


        # 构造(query, document)组合

        pairs = []


        for doc in documents:

            pairs.append(
                [
                    query,
                    doc.page_content
                ]
            )



        # 模型打分

        scores = self.model.predict(
            pairs
        )



        # 文档和分数绑定

        ranked_documents = list(
            zip(
                documents,
                scores
            )
        )



        # 从高到低排序

        ranked_documents.sort(
            key=lambda x:x[1],
            reverse=True
        )



        # 返回最高的top_k

        return [

            doc

            for doc,score in ranked_documents[:top_k]

        ]