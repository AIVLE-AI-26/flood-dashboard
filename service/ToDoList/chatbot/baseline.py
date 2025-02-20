import os
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
from geopy.distance import great_circle
import json
from math import radians, sin, cos, sqrt, atan2
from django.conf import settings


# 환경 변수 설정
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["GOOGLE_API_KEY"] = settings.MAPS_SERVICE_KEY  # 여기에 실제 Google API 키를 입력하세요.
os.environ["OPENAI_API_KEY"] = settings.OPEN_API_KEY  # 여기에 실제 OpenAI API 키를 입력하세요.

# 프로젝트의 루트 디렉토리 경로를 가져옵니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# shelters.json 및 qa_document.json 파일의 절대 경로를 생성합니다.
shelters_file_path = os.path.join(BASE_DIR, 'chatbot', 'data', 'shelters.json')
qa_document_file_path = os.path.join(BASE_DIR, 'chatbot', 'data', 'qa_document.json')

# Load the shelter document
with open(shelters_file_path, "r", encoding="utf-8") as file:
    shelters_data = json.load(file)

# Load QA document data
with open(qa_document_file_path, "r", encoding="utf-8") as file:
    qa_document = json.load(file)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def find_nearest_shelter(user_location, shelters):
    nearest_shelter = None
    min_distance = float('inf')
    
    for shelter in shelters:
        shelter_name = shelter["대피소 명칭"]
        shelter_location = (shelter["Latitude"], shelter["Longitude"])
        distance = great_circle(user_location, shelter_location).kilometers
        
        if distance < min_distance:
            min_distance = distance
            nearest_shelter = shelter_name
    
    return nearest_shelter, min_distance

def create_texts_and_metadatas(shelters_data):
    shelter_texts = []
    shelter_metadatas = []
    
    for shelter in shelters_data:
        shelter_text = (
            f"{shelter['대피소 명칭']}은(는) {shelter['구']}에 위치하고 있으며, "
            f"주소는 {shelter['주소']}입니다. "
            f"위도는 {shelter['Latitude']}이고, 경도는 {shelter['Longitude']}입니다. "
            f"최대 수용 인원은 {shelter['최대 수용 인원']}명입니다. "
            f"접근성 정보는 {shelter['접근성 정보'] if shelter['접근성 정보'] else '제공되지 않았습니다.'}."
        )
        shelter_texts.append(shelter_text)
        
        shelter_metadatas.append({
            "대피소명": shelter['대피소 명칭'],
            "주소": shelter['주소'],
            "수용인원": shelter['최대 수용 인원'],
            "구": shelter['구'],
            "위도": shelter['Latitude'],
            "경도": shelter['Longitude']
        })
    
    return shelter_texts, shelter_metadatas

def get_lat_lon(api_key, address):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': address, 'key': api_key}
    response = requests.get(endpoint, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"Error: {data['status']}")
        return None, None

# 텍스트 및 메타데이터 생성
shelter_texts, shelter_metadatas = create_texts_and_metadatas(shelters_data)

# Convert QA document data into retriever-friendly format
qa_texts = [str(qa['question']) for qa in qa_document['qa_pairs']]
qa_metadatas = [{"answer": str(qa['answer'])} for qa in qa_document['qa_pairs']]

# Combine texts and metadatas
texts = shelter_texts + qa_texts
metadatas = shelter_metadatas + qa_metadatas

# Create embeddings and build Chroma index
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)

# Create the retriever
retriever1 = vectorstore.as_retriever()

# Create the QA chain using the retriever and chat model
llm = ChatOpenAI(temperature=1.0, model_name='gpt-3.5-turbo')
qa_chain = load_qa_chain(llm, chain_type="map_reduce")

def response(message, history, additional_input_info, user_location=None, k=2):
    if history is None:
        history = []
        
    history_langchain_format = []
    history_langchain_format.append(SystemMessage(content=additional_input_info))
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    
    # Retrieve relevant documents using the retriever
    docs = retriever1.get_relevant_documents(message)

    # Debugging: Print the retrieved documents
    print("Retrieved documents:", docs)

    try:
        # Generate QA response
        result = qa_chain({"input_documents": docs, "question": message})
        final_response = result['output_text']
    except ValueError as e:
        if docs:
            final_response = docs[0].metadata['answer']
        else:
            final_response = "질문에 대한 적절한 답변을 찾을 수 없었습니다. 추가적인 정보를 제공해 주세요."

    if "내 위치는" in message:
        location_name = message.replace("내 위치는", "").strip()
        new_location = get_lat_lon(os.environ["GOOGLE_API_KEY"], location_name)
        if new_location and new_location != (None, None):
            user_location = new_location
            response_text = f"위치가 갱신되었습니다: {location_name} ({user_location[0]}, {user_location[1]})."
            final_response = response_text
        else:
            final_response = f"'{location_name}' 위치를 찾을 수 없습니다."

    if user_location:
        closest_shelter, distance = find_nearest_shelter(user_location, shelters_data)
        
        if closest_shelter:
            response_text = f"가장 가까운 대피소는 {closest_shelter}입니다. 거리는 약 {distance:.2f} km입니다."
        else:
            response_text = "가까운 대피소를 찾을 수 없습니다."
        
        final_response += f"\n\n{response_text}"
    
    history.append((message, final_response))
    
    return final_response, history
