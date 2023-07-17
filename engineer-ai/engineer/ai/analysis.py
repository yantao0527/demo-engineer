import os
import shutil
import subprocess
from pathlib import Path
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

PROJECT_WORKSPACE="/tmp/projects"

class Analysis:

    def github_clone(self, github_url):
        name = github_url.split("/")[-1].split(".")[0]
        path = Path(PROJECT_WORKSPACE)
        path.mkdir(parents=True, exist_ok=True)
        root_dir = PROJECT_WORKSPACE + "/" + name
        path = Path(root_dir)
        if path.is_dir():
            shutil.rmtree(root_dir)
        subprocess.check_call(["git", "clone", github_url, root_dir])
        return root_dir

    def index_codebase(self, root_dir):
        docs = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for file in filenames:
                try:
                    loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
                    docs.extend(loader.load_and_split())
                except Exception as e:
                    pass

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(disallowed_special=())
        DATASET_PATH=os.getenv("ACTIVELOOP_PATH")
        db = DeepLake.from_documents(docs, dataset_path=DATASET_PATH, embedding=embeddings)
        print(DATASET_PATH)

    def question(self, questions):
        embeddings = OpenAIEmbeddings(disallowed_special=())
        DATASET_PATH=os.getenv("ACTIVELOOP_PATH")
        db = DeepLake(
            dataset_path=DATASET_PATH,
            read_only=True,
            embedding_function=embeddings,
        )
        retriever = db.as_retriever()
        retriever.search_kwargs["distance_metric"] = "cos"
        retriever.search_kwargs["fetch_k"] = 100
        retriever.search_kwargs["maximal_marginal_relevance"] = True
        retriever.search_kwargs["k"] = 10

        # def filter(x):
        #     # filter based on source code
        #     if "com.google" in x["text"].data()["value"]:
        #         return False

        #     # filter based on path e.g. extension
        #     metadata = x["metadata"].data()["value"]
        #     return "scala" in metadata["source"] or "py" in metadata["source"]

        # # turn on below for custom filtering
        # retriever.search_kwargs['filter'] = filter

        model = ChatOpenAI(model_name="gpt-3.5-turbo")  # switch to 'gpt-4'
        qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

        chat_history = []
        for question in questions:
            result = qa({"question": question, "chat_history": chat_history})
            chat_history.append((question, result["answer"]))
        return chat_history


