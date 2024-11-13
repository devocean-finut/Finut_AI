import json

def merge_terms_with_excessive_spaces(input_filename, output_filename, max_spaces=3):
    # JSON 파일을 불러오기
    with open(input_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 수정된 JSON 데이터를 저장할 리스트 생성
    modified_data = []
    previous_entry = None

    for entry in data:
        # term의 공백 수가 max_spaces보다 많으면 불완전한 항목으로 판단
        if entry['term'].count(" ") >= max_spaces:
            if previous_entry:
                # 이전 항목의 description에 현재 항목의 description을 이어붙임
                previous_entry['description'] += " " + entry['description']
        else:
            # 완전한 term 항목이라면 수정 리스트에 추가
            modified_data.append(entry)
            previous_entry = entry

    # 수정된 내용을 출력 파일에 저장
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(modified_data, file, ensure_ascii=False, indent=4)

# 함수 호출
file_input = "economy_ver2.json"
file_output = "economy_ver3.json"
merge_terms_with_excessive_spaces(file_input, file_output)
