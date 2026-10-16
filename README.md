# 구소라 한의사의 피부·체형 이야기

후한의원 천안점 구소라 대표원장의 질환 정보 사이트입니다.

## 구조
- `content/` — 페이지 원고(HTML 조각). 맨 위 `<!--meta {...} -->`에 제목·설명·수정일을 적습니다.
- `assets/` — 디자인(CSS), 자가체크 스크립트, 이미지
- `build.py` — 원고에 공통 헤더·푸터·구조화 데이터(JSON-LD)를 붙여 `docs/`에 완성본을 만듭니다.
- `docs/` — 실제 공개되는 사이트 (GitHub Pages가 이 폴더를 공개)

## 글 고치는 법
1. `content/` 안 파일을 수정 (수정했으면 meta의 `updated` 날짜도 바꾸기)
2. `python3 build.py` 실행
3. 커밋·푸시하면 1~2분 뒤 사이트에 반영

## 새 질환 페이지 추가
기존 질환 파일(예: `content/20-acne.html`)을 복사해 `path`, 제목, 내용을 바꾸고,
메인(`content/00-index.html`)의 질환 카드에 링크를 추가합니다.

## 채워야 할 곳
- 건물 랜드마크: `content/11-clinic.html`
- 네이버 플레이스·블로그·인스타그램 주소: `build.py`의 `SITE`
- 도메인을 사면 `build.py`의 `base_url` 교체
