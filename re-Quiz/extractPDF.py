import pdfplumber
import re
import json

pdf_path = "./2023_경제금융용어 700선-게시(저용량).pdf"

terms_data = []

ignore_pattern = re.compile(r'^[가-힣]+\s+[ㄱ-ㅎ]$|\b[ㄱ-ㅎ]\b|\d+$')

with pdfplumber.open(pdf_path) as pdf:
    for page_number in range(16, len(pdf.pages)-3):
        page = pdf.pages[page_number]
        text = page.extract_text()

        lines = text.split('\n')
        current_term = None
        current_description = []

        for line in lines:
            # 무시할 패턴에 해당하면 스킵
            if ignore_pattern.match(line):
                continue

            # '연관검색어'가 나왔을 경우 현재 설명을 저장하고 새로운 용어로 넘어감
            if "연관검색어" in line:
                if current_term and current_description:
                    terms_data.append({
                        "term": current_term,
                        "description": " ".join(current_description).strip()
                    })
                current_term = None
                current_description = []
                continue

            # 경제금융용어가 없으면, 현재 줄을 용어로 인식
            if not current_term:
                current_term = line.strip()
            else:
                # '연관검색어'가 나오기 전까지는 설명으로 인식
                current_description.append(line.strip())

            # 마지막 용어와 설명 저장
        if current_term and current_description:
            terms_data.append({
                "term": current_term,
                "description": " ".join(current_description).strip()
            })

json_output = json.dumps(terms_data, ensure_ascii=False, indent=4)

with open("economy_ver1.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_output)

print("추출 완료")