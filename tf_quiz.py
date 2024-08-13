import json
import pandas as pd
import requests


def generate_quiz_prompt_with_ollama(term, description):
    prompt = f"""
    I want you to generate a quiz question and an answer based on the following economic term and its description.
    Make sure that all questions and answers are writen in Korean!!
    
    Term: {term}
    Description: {description}
        
    퀴즈 예시와 구체적인 설명을 해줄게.
    
    true/false 문제
    description에 있는 내용을 바탕으로 문장을 만들고, 해당 문장이 term에 관한 설명이 맞는지 true or false로 답을 내줘.
    
    다음은 해당 문제 유형에 대한 예시야:
    - term: "52주 신고가"
    - description: "52주 신고가는 특정 주식이 지난 52주(1년) 동안 기록한 가장 높은 주가를 말해요."
    - Question: “52주 신고가는 특정 주식이 지난 52주(1년) 동안 기록한 가장 높은 주가이다.”
    - Answer: true
    
    - term: "DTI"
    - description: "#DTI 🏷️ DTI(Debt to Income : 총부채상환비율)는 연 소득 대비 금융비용 부담률을 의미합니다. 내가 가진 모든 대출의 원리금 상환금액을 합쳐 따지는 DSR보다는 유한 기준입니다.”
    - question: “총부재상환비율인 DTI는 내가 가진 모든 대출의 원리금 상환금액을 합쳐 따지는 DSR보다 엄격한 기준이다.”
    - answer: false
     
        
    Format the output as follows:
    Question: <your generated question>
    Answer: <your generated answer>
    """

    response = requests.post(
        "http://localhost:11434/api/generate",  # 포트 번호 11434 사용
        json={"model": "llama3", "prompt": prompt},  # 모델 이름을 실제로 사용 중인 모델로 설정
        stream=True  # 스트리밍 응답을 받기 위해 stream=True 추가
    )

    # 스트리밍된 응답을 한 줄씩 받아서 처리
    full_response = ""
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            # print(decoded_line)  # 각 줄을 출력해 확인
            json_data = json.loads(decoded_line)
            if "response" in json_data:
                full_response += json_data["response"]

    print("Full response:", full_response)

    # "Question:" 다음에 시작하는 텍스트로 질문과 답을 분리
    question_answer_split = full_response.split("Answer:")

    question = question_answer_split[0].strip()
    answer = ""

    if len(question_answer_split) > 1:
        answer = question_answer_split[1].strip()

    return question, answer


# JSON 파일 데이터 로드
with open('economy_terms_modified.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 퀴즈 생성 및 엑셀 저장 준비
quiz_data = []

for entry in data:
    term = entry['term']
    description = entry['description']

    # 퀴즈 생성 시작 시 term을 출력
    print(f"Generating quiz for term: {term}")

    # Ollama 모델로 퀴즈 생성
    question, answer = generate_quiz_prompt_with_ollama(term, description)

    # 데이터 리스트에 저장
    quiz_data.append({
        "Term": term,
        "Description": description,
        "Question": question,
        "Answer": answer
    })

df = pd.DataFrame(quiz_data)
excel_path = '/Users/user/Desktop/Finut_Quiz_tf.xlsx'
df.to_excel(excel_path, index=False)

print(f"으아아아아 끝!!")
