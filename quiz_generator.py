from transformers import LlamaForCausalLM, LlamaTokenizer
import json
import pandas as pd

model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct" # llama3 사용
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name)

# 텍스트 생성 함수
def generate_quiz_prompt(term, description):
    prompt = f"""
    I want you to generate a quiz question and an answer based on the following economic term and its description.
    
    Term: {term}
    Description: {description}
    
    make a quiz for me!
    
    Format the output as follows:
    Question: <your generated question>
    Answer: <your generated answer>
    """

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=200)

    # 출력에서 질문과 답을 분리
    generated_text = tokenizer.batch_decode(outputs[0], skip_special_tokens=True)

    # "Question:" 다음에 시작하는 텍스트로 질문과 답을 분리
    question_answer_split = generated_text.split("Answer:")

    question = question_answer_split[0].strip()
    answer = question_answer_split[1].strip() \
        if len(question_answer_split) > 1 else "Answer not found"

    return question, answer

# JSON 파일 데이터 로드
with open('economy_terms_modified.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 퀴즈 생성 및 엑셀 저장 준비
quiz_data = []

for entry in data:
    term = entry['term']
    description = entry['description']

    # llama 모델로 퀴즈 생성
    question, answer = generate_quiz_prompt(term, description)

    # 데이터 리스트에 저장
    quiz_data.append({
        "Term": term,
        "Description": description,
        "Question": question,
        "Answer": answer
    })

df = pd.DataFrame(quiz_data)

excel_path = '/Users/user/Desktop/Finut_Quiz.xlsx'
df.to_excel(excel_path, index=False)

print(f"으아아아아 끝!!")
