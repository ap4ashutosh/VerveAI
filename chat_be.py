from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
import boto3


region = 'us-east-1'
service = 'aoss'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


vector = OpenSearch(
   hosts = [{'host': aoss-example-1234.us-east-1.aoss.amazonaws.com', 
             'port': 443}],
   http_auth = awsauth,
   use_ssl = True,
   verify_certs = True,
   http_compress = True,
   connection_class = RequestsHttpConnection
)

index_body = {
  'settings': {
    "index.knn": True
  },
  "mappings": {
    "properties": {
      "osha_vector": {
        "type": "knn_vector",
        "dimension": 1536,
        "method": {
          "engine": "faiss",
          "name": "hnsw",
          "space_type": "l2"
        }
      }
    }
  }
}


response = vector.indices.create('aoss-index', body=index_body)

from langchain-community.embeddings import TitanTextEmbeddings

embeddings = TitantextEmbeddings()

from langchain.vectorstores import OpenSearchVectorSearch


vector = OpenSearchVectorSearch(
  embedding_function = embeddings,
  index_name = 'aoss-index',
  http_auth = awsauth,
  use_ssl = True,
  verify_certs = True,
  http_compress = True, # enables gzip compression for request bodies
  connection_class = RequestsHttpConnection,
  opensearch_url=opensearch_url="https://aoss-example-1234.us-east-1.aoss.amazonaws.com"
)

import boto3


s3_resource = boto3.resource('s3', region_name="us-east-1")
s3_bucket = s3_resource.Bucket("my-sample-osha-bucket")
s3_bucket_files = []
for s3_object in s3_bucket.objects.all():
    <more magic for here below>
    loader = S3FileLoader(bucket_name, file_key)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,
                                                    chunk_overlap = 20,
                                                    length_function = len,
                                                    is_separator_regex = False,)
    pages = loader.load_and_split(text_splitter=text_splitter)
    vector.add_documents(
    documents = pages,
    vector_field = "osha_vector"
    )

docs = vector.similarity_search_by_vector(
  "What is the standard height where fall protection is required?",
  vector_field="osha_vector",
  text_field="text",
  metadata_field="metadata",
)


​​docs_dict = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in docs]
data = ""
for doc in docs_dict:
    data += doc['page_content'] + "\n\n"

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


llm = OpenAI()
prompt = PromptTemplate(
  input_variables=["question", "data"],
  template="""Using the data below, answer the question provided.
  question: {question}
  data: {data}
  """,
)


chain = LLMChain(llm=llm, prompt=prompt)
llm_return_data = chain.run({'question': question, 'data': data})
