# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox
def getExcelData(workbook, columnDictionary, SheetName='Sheet1'):
    ws = workbook.get_sheet_by_name(SheetName)
    last_row = ws.max_row

    # 반환 리스트
    recList = []

    # 엑셀 정합성 체크
    validExcel = True;
    errType = 0;
    errColumns = ""
    for xlrow in ws.iter_rows(row_offset=1):
        if xlrow[0].row > last_row:
            break;
        else:
            col_idx = 0
            for cell in xlrow:
                if columnDictionary[col_idx]['colMandatoryYN'] == 'Y' and (cell.value == None or cell.value == ''):
                    validExcel = False
                    errType = 1
                    errColumns += ", " + cell.column + str(cell.row)
                elif int(columnDictionary[col_idx]['colMaxLength']) > 0 and len(cell.value) > int(
                        columnDictionary[col_idx]['colMaxLength']):
                    validExcel = False
                    errType = 2
                    errColumns += ", " + cell.column + str(cell.row)

                col_idx += 1

    if validExcel == False:
        if errType == 1:
            QMessageBox.warning(None, "엑셀파일 에러",
                                "엑셀업로드에 에러가 발생하였습니다.\n\n"
                                "{0} Cell은 빈값을 허용하지 않습니다.".format(errColumns[2:]),
                                QMessageBox.Close)
        elif errType == 2:
            QMessageBox.warning(None, "엑셀파일 에러",
                                "엑셀업로드에 에러가 발생하였습니다.\n\n"
                                "{0} Cell의 값이 허용길이를 초과하였습니다".format(errColumns[2:]),
                                QMessageBox.Close)

    else:
        for xlrow in ws.iter_rows(row_offset=1):
            if xlrow[0].row > last_row:
                break;
            else:
                col_idx = 0
                # 리스트에 추가될 레코드
                record = {}
                for cell in xlrow:
                    record[columnDictionary[col_idx]['colName']] = cell.value
                    col_idx += 1
                recList.append(record)

    return recList
