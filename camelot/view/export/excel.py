#  ==================================================================================
#
#  Copyright (C) 2007-2008 Conceptive Engineering bvba. All rights reserved.
#  www.conceptive.be / project-camelot@conceptive.be
#
#  This file is part of the Camelot Library.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  this file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
#
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact
#  project-camelot@conceptive.be.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#  For use of this library in commercial applications, please contact
#  project-camelot@conceptive.be
#
#  ==================================================================================

from pyExcelerator import *
import pickle
import time
import datetime

titleFont = Font()              # initializing titleFont Object
headerFont = Font()             # initializing headerFont Object
cellFont = Font()               # initializing cellFont Object

titleFont.name = 'Arial'        # Setting Fonts Name
headerFont.name = 'Arial'
cellFont.name = 'Arial'

titleFont.bold = True           # Setting title font to bold
headerFont.bold = True          # Setting column header font to bold
cellFont.bold = False           # Setting cell font to bold

titleFont.height = 240          # 12*20 = 240 Font Size
headerFont.height = 220         # 11*20 = 240 Font Size
cellFont.height = 220           # 11*20 = 240 Font Size

brdLeft = Borders()                # Defining border which is around header
brdLeft.left = 0x01

brdRight = Borders()                # Defining border which is around header
brdRight.right = 0x01

brdTop = Borders()                # Defining border which is around header
brdTop.top = 0x01

brdBottom = Borders()                # Defining border which is around header
brdBottom.bottom = 0x01

brdTopLeft = Borders()
brdTopLeft.top = 0x01
brdTopLeft.left = 0x01

brdBottomLeft = Borders()
brdBottomLeft.bottom = 0x01
brdBottomLeft.left = 0x01

brdBottomRight = Borders()
brdBottomRight.bottom = 0x01
brdBottomRight.right = 0x01

brdTopRight = Borders()
brdTopRight.top = 0x01
brdTopRight.right = 0x01

dateStyle = XFStyle()


titleStyle = XFStyle()
headerStyle = XFStyle()
cellStyle = XFStyle()
dateStyle = XFStyle()

leftCellStyle = XFStyle()
rightCellStyle = XFStyle()
bottomCellStyle = XFStyle()
topleftCellStyle = XFStyle()
bottomleftCellStyle = XFStyle()
bottomrightCellStyle = XFStyle()
toprightCellStyle = XFStyle()

titleStyle.font = titleFont
headerStyle.font = headerFont
headerStyle.borders = brdTop
cellStyle.font = cellFont

topleftCellStyle.font = headerFont
topleftCellStyle.borders = brdTopLeft

bottomleftCellStyle.font = cellFont
bottomleftCellStyle.borders = brdBottomLeft

bottomrightCellStyle.font = cellFont
bottomrightCellStyle.borders = brdBottomRight

toprightCellStyle.font = headerFont
toprightCellStyle.borders = brdTopRight

leftCellStyle.borders = brdLeft
leftCellStyle.font = cellFont

rightCellStyle.borders = brdRight
leftCellStyle.font = cellFont

bottomCellStyle.borders = brdBottom
bottomCellStyle.font = cellFont

pat1 = Pattern()
pat1.pattern = Pattern.SOLID_PATTERN
pat1.pattern_fore_colour = 0x16
headerStyle.pattern = pat1
topleftCellStyle.pattern = pat1
toprightCellStyle.pattern = pat1

class clsExcel:
    def createExcel(self, filename, title, headerList, dataList):
        try:
            w = Workbook()
            ws = w.add_sheet('Sheet1')
            ## Writing Title
            ws.write(0, 0, title, titleStyle)                   # Writing Title
            ws.col(0).width = len(title) * 400                  # Setting cell width
            ## Writing Header
            ws.write(2, 0 , 'Serial No.', topleftCellStyle)
            if ( ws.col(0).width < ws.col(0).width * 300):
                ws.col(0).width = len('Serial No.') * 300       # Setting cell width
            myDataTypeDict = {}            # dictionary of datatype, {columnnumber, Datatype}
            myPrecisionDict = {}        # dictionary of precision , {columnnumber, Precision}
            myLengthDict = {}           # dictionary of length , {columnnumber, length}
            myFormatDict = {}           # dictionary of dateformat , {columnnumber, format}
            n = 0
            for desc in headerList:
                lst =  desc[1]
                if n+1 != len(headerList):      # Setting Border
                    ws.write(2, n + 1, lst['name'], headerStyle)
                else:
                    ws.write(2, n + 1, lst['name'], toprightCellStyle)
                if len(lst['name']) < 8:
                    ws.col(n + 1).width = 8 *  375
                else:
                    ws.col(n + 1).width = len(lst['name']) *  375
                myDataTypeDict[ n + 1 ] = lst["python_type"]
                if lst["python_type"] == float:
                    myPrecisionDict [ n + 1 ] = lst["precision"]    #Populating precision dictionary
                elif lst["python_type"] == datetime.date:
                    myFormatDict [ n + 1 ] = lst["format"]          #Populating date Format dictionary
                elif lst["python_type"] == str:
                    myLengthDict [ n + 1 ] = lst["length"]          #Populating Column Length dictionary
                n = n + 1
            ## Writing Data
            row = 3
            column = 1
            valueAddedInSize = 0
            formatStr = '0'
            for dictCounter in dataList:                       # iterating the dataList, having dictionary
                column = 1
                cellStyle.num_format_str = '0'
                if row - 2 != len(dataList):
                    ws.write(row , 0, row - 2 , leftCellStyle)
                else:
                    ws.write(row , 0, row - 2 , bottomleftCellStyle)
                for i in range( 0 , len(dictCounter)): #for i in dictCounter:
                    valueAddedInSize = 0
                    val = dictCounter[i]
                    if val != None:
                        if myDataTypeDict.has_key(column) == True:
                            if myLengthDict.get(column) != None:
                                if len(val) > myLengthDict[ column ]:
                                    val = val[0:myLengthDict[ column ]]
                            elif myDataTypeDict[ column ] == str:
                                formatStr = '0'
                            elif myDataTypeDict[ column ] == int:
                                formatStr = '0'
                            elif myDataTypeDict[ column ] == float:
                                formatStr = '0.'
                                for j in range( 0 , myPrecisionDict[ column ]):
                                    formatStr += '0'
                                valueAddedInSize = len(formatStr) # To fit the cell width + 1 (of dot(.))
                            elif myDataTypeDict[ column ] == datetime.date:
                                formatStr = myFormatDict[column]
                                val = datetime.datetime( day = val.day, year = val.year, month = val.month)
                            elif myDataTypeDict[ column ] == bool:
                                formatStr = '0'
                            else:
                                formatStr = '0'
                        cellStyle.num_format_str = formatStr
                        bottomCellStyle.num_format_str = formatStr
                        rightCellStyle.num_format_str = formatStr
                        bottomrightCellStyle.num_format_str = formatStr
                    elif val == None:
                        val = ' '
                    if  i + 1 == len(dictCounter) and row - 2 != len(dataList):            #right column
                        ws.write(row , column, val , rightCellStyle)
                    elif row - 2  == len(dataList)  and i  < len(dictCounter) - 1:         #Bottom Row
                        ws.write(row , column, val , bottomCellStyle)
                    elif row - 2  == len(dataList)  and i  == len(dictCounter) - 1 :       #Bottom Right
                        ws.write(row , column, val , bottomrightCellStyle)
                    else:
                        if val != None:
                            ws.write(row , column, val , cellStyle)
                    if ws.col(column).width < (len(unicode( val )) )* 300:
                        ws.col(column).width = (len(unicode( val )) + valueAddedInSize )* 300
                    column = column + 1
                row = row + 1
            w.save(filename)
        except Exception , e:
            print e
            print 'Exception in function createExcel'


if __name__ == '__main__':
    arguments = {}
    arguments = pickle.load(open('Purchase order.pickle', 'rb'))

    dataList = list(arguments['data'])
    headerList = list(arguments['columns'])
    title = arguments['title']

    objExcel = clsExcel()
    objExcel.createExcel( title, headerList, dataList )