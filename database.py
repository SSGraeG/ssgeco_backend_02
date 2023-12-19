from pymysql import connect
from datetime import datetime
import shutil
from flask import Flask, json, jsonify
from os import path
import pymysql

# from datetime import datetime


connectionString = {
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'eco',
    # 'user': 'user1',
    # 'password': '1234',
    'user': 'root',
    # 'password': '1234',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}


def idCheck(user_id, pwd):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user " + "where email = %s and password = %s;"
            cursor.execute(sql, [user_id, pwd])
            result = cursor.fetchall()

            return result
    except Exception as e:
        print(e)
def id_duplicate_check(email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user where email = %s;"
            cursor.execute(sql,[email])
            result = cursor.fetchone()

            return result
    except Exception as e:
        print(e)
def getAll():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM USER"
            cursor.execute(sql)
            result = cursor.fetchall()
            print("dd" ,result)
            return result
    except Exception as e:
        print(e)

def getMyItem(user_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM item where user_id = %s;"
            cursor.execute(sql, [user_id])
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)


def getItems(sort, keyword):
    try:
        query = "SELECT * FROM item"

        # Conditionally filter by keyword
        if keyword:
            query += f" WHERE name LIKE '%{keyword}%' OR content LIKE '%{keyword}%'"

        if sort == "priceDown":
            query += " ORDER BY price DESC"
        elif sort == "priceUp":
            query += " ORDER BY price ASC"
        else:
            query += " ORDER BY startTime DESC"

        with connect(**connectionString) as con:
            cursor = con.cursor()
            cursor.execute(query)
            itemInfo = cursor.fetchall()
            cursor.close()

            # columns = [desc[0] for desc in cursor.description]
            # data = [dict(zip(columns, row)) for row in user_info]
        if not itemInfo:
            return [], 200, {'Content-Type': 'application/json'}

        return itemInfo, 200, {'Content-Type': 'application/json'}


    except Exception as e:
        print(e)


# 메인페이지에서 1번상품을 들어가면 1번상품에 해당하는 내용이 나와야하기떄문에 id인자와 쿼리문 살짝 수정
def getItemDetails(id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "select * from item where id = %s"
            cursor.execute(sql, (id,))
            itemDetails = cursor.fetchone()
            cursor.close()

            # columns = [desc[0] for desc in cursor.description]
            # data = [dict(zip(columns, row)) for row in user_info]
        return itemDetails, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(e)


def addUserInfo(email, name, password, address):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "INSERT INTO user (email, name, password, address) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (email, name, password, address))
            user_info = cursor.fetchall()
            con.commit()

        return user_info, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return {"error": "사용자 정보 추가에 실패했습니다."}, 500, {'Content-Type': 'application/json'}


# 마이페이지에서 내 게시글 내역
def getMyItem(user_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM item where user_id = %s;"
            cursor.execute(sql, [user_id])
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)

    # 마이페이지에서 내 구매내역


def getBuyItem(user_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            # user_id로 history item_id를 조회하고, 조회된 item_id로 item테이블의 데이터를 출력하는 쿼리
            # sql = "SELECT * from history where user_id = %s;"
            sql = "SELECT item.* FROM item INNER JOIN history ON item.id = history.item_id WHERE history.user_id = %s;"
            cursor.execute(sql, [user_id])
            result = cursor.fetchall()
            print(result)
            return result
    except Exception as e:
        print(e)


def addItemInfo(itemName, itemContent, itemPrice, itemImage, endTime, userId):
    with connect(**connectionString) as con:
        cursor = con.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # SQL 쿼리 수정: 플레이스홀더를 사용하여 SQL 인젝션을 방지합니다.
        sql = "INSERT INTO item (name, content, price, image, endTime, startTime, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (itemName, itemContent, itemPrice, itemImage, endTime, now, userId))
        con.commit()

    return "경매물품 등록 성공", 200


# database.py
def getItemDetails(id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "select * from item where id = %s"
            cursor.execute(sql, (id,))
            itemDetails = cursor.fetchone()
            cursor.close()

            # columns = [desc[0] for desc in cursor.description]
            # data = [dict(zip(columns, row)) for row in user_info]
        return itemDetails, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(e)


def updatePrice(id, price, new_price):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "UPDATE item SET price = %s WHERE id = %s"
            cursor.execute(sql, (new_price, id))
            con.commit()
            cursor.close()
            return {"message": "입찰되었습니다."}, 200

    except Exception as e:
        print(e)
        return {"message": "가격 업데이트에 실패했습니다."}, 500


def insertPrehistory(itemId, userId, endTime):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            formatted_date = datetime.strptime(endTime[:-4], '%a, %d %b %Y %H:%M:%S')
            formatted_date_for_mysql = formatted_date.strftime('%Y-%m-%d %H:%M:%S')
            # endTime = datetime.strptime(endTime, '%a, %d %b %Y %H:%M:%S %Z')
            sql = "INSERT INTO prehistory (item_id, user_id, endTime) VALUES (%s, %s, %s)"
            cursor.execute(sql, (itemId, userId, formatted_date_for_mysql))
            con.commit()
            cursor.close()
            return {"message": "거래 저장"}, 200

    except Exception as e:
        print(e)
        return {"message": "거래 실패"}, 500