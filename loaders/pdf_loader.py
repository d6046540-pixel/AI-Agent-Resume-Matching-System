from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path: str):
	"""Load PDF and return list of Document objects using PyPDFLoader."""
	loader = PyPDFLoader(file_path)

	documents = loader.load()

	return documents

