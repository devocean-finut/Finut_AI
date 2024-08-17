import pandas as pd

# 엑셀 파일을 읽어온다
file_path = "/Users/user/Desktop/Finut_Quiz_multiple_choice.xlsx"
df = pd.read_excel(file_path)

# Description 열에서 Term 열의 내용을 삭제하는 함수
def remove_description_prefix(row):
    term_with_hash = f"#{row['Term']}"
    description = row['Description']

    if description.startswith(term_with_hash):
        return description[len(term_with_hash):].lstrip()
    else:
        return description

# Description 열에서 Term 열의 내용을 삭제하고 결과를 저장
df['Description'] = df.apply(remove_description_prefix, axis=1)

# 수정된 데이터를 새로운 엑셀 파일로 저장
output_file_path = "/Users/user/Desktop/Finut_Quiz_multiple_choice_update.xlsx"
df.to_excel(output_file_path, index=False)

print(f"수정된 엑셀 파일이 저장되었습니다: {output_file_path}")
