# dbf-euckr-to-utf8

## 1. .dbf file format

Byte | Contents | Meaning
-- | -- | --
0 | 1 byte | Valid dBASE for DOS file; bits 0–2 indicate version number, bit 3   indicates the presence of a dBASE for DOS memo file, bits 4–6 indicate the   presence of a SQL table, bit 7 indicates the presence of any memo file   (either dBASE m PLUS or dBASE for DOS)
1–3 | 3 bytes | Date of last update; formatted as YYMMDD
4–7 | 32-bit number | Number of records in the database file
8–9 | 16-bit number | Number of bytes in the header
10–11 | 16-bit number | Number of bytes in the record
12–13 | 2 bytes | Reserved; fill with 0
14 | 1 byte | Flag indicating incomplete   transactionhttps://en.wikipedia.org/wiki/.dbf#cite_note-10
15 | 1 byte | Encryption flaghttps://en.wikipedia.org/wiki/.dbf#cite_note-11
16–27 | 12 bytes | Reserved for dBASE for DOS in a multi-user environment
28 | 1 byte | Production .mdx file flag; 1 if there is a production .mdx file, 0 if not
29 | 1 byte | Language driver ID
30–31 | 2 bytes | Reserved; fill with 0
32–n | 32 bytes each | array of field descriptors (see below for layout of descriptors)
n + 1 | 1 byte | 0x0D as the field descriptor array terminator

출처 : https://en.wikipedia.org/wiki/.dbf


![Untitled](https://user-images.githubusercontent.com/49121847/135183659-6220e9ad-f82d-49bb-a8ae-3767225b3ee6.png)
Z_KAIS_TL_SPBD_BULD_36110.dbf

## 2. 프로그램 구현

위 이미지는 Z_KAIS_TL_SPBD_BULD_36110.dbf의 앞 부분이다. 위의 표와 비교하며 필요한 부분만 설명하겠다. 

- `1-3 byte`에는 마지막 업데이트 날짜가 YYMMDD 형식으로 저장되어 있다. 이 파일은 2015년 9월 1일에 마지막으로 업데이트 되었다.
- `4-7 byte`에는 데이터베이스 파일의 레코드 수가 저장되어 있다. 이 파일에는 0xD9F4개(55796개)의 레코드가 저장되어 있다.
- `8-9 byte`에는 헤더의 바이트 수가 저장되어 있다. 예시 파일 헤더의 바이트 수는 0x03E1(993개)다. 헤더가 0x03E0까지 저장되어 있는 것을 보고 확인할 수 있다.
- `10-11 byte`에는 레코드의 바이트 수가 저장되어 있다. 예시 파일의 바이트 수는 0x025C(604개다).
- `32-n byte`에는 (각각 32바이트) 각 필드에 대한 정보가 저장된다. 예시 파일에서도 확인할 수 있듯이 0x00000021 ~ 0x000003DF 까지 각 필드에 대한 정보가 저장되어있다.
- `n+1 byte`에는 필드에 대한 정보를 저장하는 부분이 끝났음을 표시하는 0x0D가 저장된다. 위 이미지에서 0x000003E0 에 0x0D가 저장되어 있는 것을 확인할 수 있다.
- 이후 `n+2 byte`부터 데이터가 저장된다. 맨 앞부분은 BLANK(0x20)로 시작한다. 헤더에 저장된 각 필드별 고정 길이, 레코드의 고정 길이에 맞게 읽고, 정해진 길이만큼 데이터가 저장되지 않으면 나머지 부분은 BLANK(0x20)으로 채워진다.

.dbf 파일의 인코딩 방식을 바꿀 때는 구조를 생각하며 바꿔야 한다. 우선 파일의 각 필드의 바이트 수를 읽는다. 필드의 바이트 수의 합이 레코드의 길이 이므로, 레코드의 길이는 따로 읽을 필요가 없다. 이후 레코드를 순회하며 각 필드마다 euc-kr로 decoding한 후, utf-8로 encoding 한다. 한글의 경우 euc-kr에서 utf-8로 인코딩 방법을 바꾸면 바이트 수가 늘어난다. 각 필드를 인코딩 할 때, 기존 길이보다 길어졌다면 뒷 부분의 BLANK 중 넘치는 부분만 잘라서 저장하면 된다.

이 프로그램은 위의 원리로 작성되었다. 이 프로그램은 function으로 작성하여 다른 program에서 호출할 수 있도록 한다. 매개변수는 인코딩하고자 하는 파일의 경로(FILEPATH)이고 output으로 인코딩이 성공할 경우 true, 실패할 경우 false를 리턴한다.

error case와 그데 대한 처리 방법 및 test program은 현재 작성하고 있는 프로그램을 구현한 후 추가할 예정이다.