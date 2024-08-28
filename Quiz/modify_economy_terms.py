import json

# JSON 파일 읽기
with open('economy_terms.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 내용 수정
for entry in data:
    description = entry['description']

    # 단어 '구독' 제거
    if description.startswith('구독'):
        description = description[len("구독"):].strip()

    # 뒤에 쓸데없는 첨언 제거
    cutoff_phrase = "막막한 경제 공부, 머니레터로 시작하세요 매주 수요일 잘쓸레터에서 만나요"
    if cutoff_phrase in description:
        description = description.split(cutoff_phrase)[0].strip()

    # 수정된 description 다시 저장
    entry['description'] = description

# JSON 파일로 저장
with open('economy_terms_modified.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("JSON 파일이 성공적으로 수정되었습니다.")
