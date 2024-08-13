import json
import pandas as pd
import requests


def generate_quiz_prompt_with_ollama(term, description):
    prompt = f"""
    I want you to generate a quiz question and an answer based on the following economic term and its description.
    Make the questions and answers in Korean!!

    Term: {term}
    Description: {description}

    퀴즈 예시와 구체적인 설명을 해줄게.

    description에 있는 내용으로 문장을 만들어 알맞은 term을 맞추는 객관식 문제를 만들어줘.
    각 선지는 option1, 2, 3에 저장해줘.

    - term: "덤핑"
    - description: "덤핑은 물건을 저가에 대량으로 와르르 팔아버리는 걸 뜻하는 단어예요."
    - Question: “쓰레기를 갖다 버리듯이 물건을 저가에 대량으로 와르르 팔아버리는 걸 뜻하는 단어는?”
    - Answer: “덤핑”
    - Option1: “분리수거”
    - Option2: “덤핑”
    - Option3: “트래싱”

    term과 description 쌍에 대해 최소 1개 이상의 question/answer를 만들어줘. 

    Format the output as follows:
    Question: <your generated question>
    Answer: <your generated answer>
    Option1: <your generated option 1>
    Option2: <your generated option 2>
    Option3: <your generated option 3>
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
    option1 = option2 = option3 = ""

    if len(question_answer_split) > 1:
        answer_part = question_answer_split[1].strip()

        # 옵션이 있는 경우와 없는 경우 구분
        if "Option1:" in answer_part:
            answer, options = answer_part.split("Option1:", 1)
            answer = answer.strip()

            # 옵션 분리
            option1 = options.strip()
            if "Option2:" in option1:
                option1, option2 = option1.split("Option2:", 1)
                option1 = option1.strip()

                if "Option3:" in option2:
                    option2, option3 = option2.split("Option3:", 1)
                    option2 = option2.strip()
                    option3 = option3.strip()
        else:
            answer = answer_part  # Option1이 없는 경우 answer만 할당

    return question, answer, option1, option2, option3


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
    question, answer, option1, option2, option3 = generate_quiz_prompt_with_ollama(term, description)

    # 데이터 리스트에 저장
    quiz_data.append({
        "Term": term,
        "Description": description,
        "Question": question,
        "Answer": answer,
        "Option1": option1,
        "Option2": option2,
        "Option3": option3
    })

df = pd.DataFrame(quiz_data)
excel_path = '/Users/user/Desktop/Finut_Quiz_multiple_choice.xlsx'
df.to_excel(excel_path, index=False)

print(f"으아아아아 끝!!")
