import pandas as pd

# 엑셀 파일을 읽어온다
file_path = "/Users/user/Desktop/Finut_Quiz_tf.xlsx"
df = pd.read_excel(file_path)

# Question열의 첫 번째 문장을 제거하는 함수
def remove_first_sentence(text):
    if pd.notna(text):  # 텍스트가 NaN이 아닌 경우
        # \n을 기준으로 첫 번째 문장을 분리하고 나머지를 반환
        return text.split('\n', 1)[-1] if '\n' in text else text
    return text  # NaN이거나 \n이 없는 경우 그대로 반환

# Question 열에서 "Question: "을 제거하는 함수
def remove_question_prefix(text):
    if pd.notna(text) and text.startswith("Question: "):  # 텍스트가 NaN이 아니고 "Question: "으로 시작하는지 확인
        return text[len("Question: "):]  # "Question: "을 제거하고 나머지 반환
    return text  # 조건에 맞지 않으면 원본 텍스트 반환

# 문자열에서 양쪽에 있는 "를 제거하는 함수
def remove_quotes(text):
    if pd.notna(text) and text.startswith('"') and text.endswith('"'):
        return text[1:-1]  # 첫 문자와 마지막 문자를 제거
    return text  # 조건에 맞지 않으면 원본 텍스트 반환

def remain_first_sentence(text):
    if pd.notna(text):
        return text.split('\n', 1)[0] if '\n' in text else text
    return text

# 각 행의 Question 열에 대해 첫 번째 문장을 제거한다
df['Question'] = df['Question'].apply(remove_first_sentence)
df['Question'] = df['Question'].apply(remove_first_sentence)

# 각 행의 Question 열에 대해 "Question: "을 제거한다
df['Question'] = df['Question'].apply(remove_question_prefix)

# Answer, Option1, Option2 열에 대해 "를 제거한다
# df['Answer'] = df['Answer'].apply(remove_quotes)
# df['Option1'] = df['Option1'].apply(remove_quotes)
# df['Option2'] = df['Option2'].apply(remove_quotes)

# Option3 열에서 첫 문장만 남긴다
#df['Option3'] = df['Option3'].apply(remain_first_sentence)
#df['Option3'] = df['Option3'].apply(remove_quotes)

# 수정된 데이터를 새로운 엑셀 파일로 저장
output_file_path = "/Users/user/Desktop/Finut_Quiz_tf.xlsx"
df.to_excel(output_file_path, index=False)

print(f"수정된 엑셀 파일이 저장되었습니다: {output_file_path}")
