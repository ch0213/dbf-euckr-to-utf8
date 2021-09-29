import dbf

BLANK = 32


def encoding_to_utf(FILEPATH):
    """
    :param FILEPATH: utf8로 인코딩할 파일의 경로
    :return:
    """
    global BLANK

    # euc-kr로 인코딩되어 있는 기존 테이블을 load & open
    euc_table = dbf.Table(FILEPATH, codepage='utf8')
    euc_table.open(dbf.READ_WRITE)

    # record의 column 별 길이를 저장한다.
    columns_length = []
    for column_name in euc_table.first_record._meta.keys():
        columns_length.append(euc_table.first_record._meta[column_name][2])

    # 테이블의 record를 euc-kr로 디코딩한 후 utf-8로 인코딩한다.
    for record in dbf.Process(euc_table):
        # 기존 euc-kr로 인코딩된 record를 대체할 새로운 record 생성한다.
        # dbf file의 record는 첫 바이트가 BLANK이므로 BLANK를 추가한다.
        utf_record = [BLANK]
        # record의 첫 부분은 BLANK이므로 시작 index를 1로 설정
        column_idx = 1
        # record의 각 column을 인코딩한다. 인코딩한 후 기존 길이보다 길어지면 기존 길이만큼만 저장한다.
        for length in columns_length:
            temp = record._data[column_idx:column_idx+length]
            column_idx = column_idx+length
            utf_record.extend(list(bytes(temp)
                              .decode("euc-kr")
                              .encode("utf8")[:length]))
        # 새로 완성된 record를 저장한다.
        record._data = bytes(utf_record)

if __name__ == "__main__":

    FILEPATH = 'data/Z_KAIS_TL_SPBD_BULD_36110.dbf'
    encoding_to_utf(FILEPATH)
