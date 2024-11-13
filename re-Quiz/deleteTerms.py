import json

def modify_json_file(input_filename, output_filename):
    # JSON 파일을 불러오기
    with open(input_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 수정할 JSON 데이터를 저장할 리스트 생성
    modified_data = []
    previous_entry = None

    for entry in data:
        # "경제금융용어 700선"을 찾으면 이전 항목의 description에 추가
        if entry['term'] == "경제금융용어 700선":
            if previous_entry:
                previous_entry['description'] += " " + entry['description']
        else:
            # 그렇지 않으면 기존 항목을 수정 리스트에 추가
            modified_data.append(entry)
            previous_entry = entry

    # 수정된 내용을 출력 파일에 다시 저장
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(modified_data, file, ensure_ascii=False, indent=4)

# JSON 파일 수정 함수 호출
file_input = "./economy_ver1.json"
file_output = "./economy_ver2.json"
modify_json_file(file_input, file_output)
