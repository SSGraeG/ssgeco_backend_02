import pymysql
from pymysql import connect
from datetime import datetime, timedelta
import pytz
from flask import Flask

app = Flask(__name__)

connectionString = {
    # 'host': '127.0.0.1',
    'host': 'eco-rds.cykey8vytdto.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'company_3',
    'user': 'admin',
    # 'user': 'root',
    # 'password': '1234',
    'password': 'password',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}

def login(email, token):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "INSERT INTO user_token (user_email, token) VALUES (%s, %s)"
            cursor.execute(sql, (email,token))
            user_info = cursor.fetchall()
            con.commit()
            app.logger.debug(user_info)
            return user_info, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        app.logger.debug(e)
        
def delete_token(token):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "DELETE FROM user_token WHERE token = %s"
            cursor.execute(sql, (token,))
            con.commit()
            return True
    except Exception as e:
        app.logger.debug(e)
        return False
    
def get_user_by_token(token):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT user_email FROM user_token WHERE token = %s"
            cursor.execute(sql, (token,))
  
            user_email = cursor.fetchone()
            # user_email = user_email[0]['user_email']
            return user_email.get('user_email')
    except Exception as e:
        app.logger.debug(e)


def get_all():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM USER"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        app.logger.debug(e)


def id_check(user_id, pwd):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user " + "where email = %s and password = %s;"
            cursor.execute(sql, [user_id, pwd])
            result = cursor.fetchall()
            return result
    except Exception as e:
        app.logger.debug(e)


def id_duplicate_check(email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user where email = %s;"
            cursor.execute(sql,[email])
            result = cursor.fetchone()
            return result
    except Exception as e:
        app.logger.debug(e)


def sign_up(email, name, password, address):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "INSERT INTO user (email, name, password, address) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (email, name, password, address))
            user_info = cursor.fetchall()
            con.commit()
            return user_info, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        app.logger.debug(e)


def get_user(email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM user where email = %s;"
            cursor.execute(sql, (email, ))
            user_info = cursor.fetchone()
            con.commit()
            return user_info
    except Exception as e:
        app.logger.debug(e)


def get_coupon():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM mileage_category where category='coupon' order by usepoint"
            cursor.execute(sql)
            coupon_list = cursor.fetchall()
            con.commit()
            return coupon_list
    except Exception as e:
        app.logger.debug(e)

from datetime import datetime

def get_user_coupon(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = ("SELECT cl.*, mc.name as category_name "
                   "FROM coupon_list cl "
                   "JOIN mileage_category mc ON cl.mileage_category_id = mc.id "
                   "WHERE cl.user_email = %s AND mc.category = 'coupon' "
                   "ORDER BY mc.usepoint")
            cursor.execute(sql, (user_email,))
            coupon_list = cursor.fetchall()

            # Format the 'expired_date' in the result set
            for coupon in coupon_list:
                coupon['expired_date'] = coupon['expired_date'].strftime('%Y-%m-%d')

            con.commit()
            print(coupon_list)
            return coupon_list
    except Exception as e:
        app.logger.debug(e)




def get_donation():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM mileage_category where category='donation' order by usepoint"
            cursor.execute(sql)
            donation_list = cursor.fetchall()
            con.commit()
            return donation_list
    except Exception as e:
        app.logger.debug(e)

# 쿠폰 전환 -> 마일리지 업데이트, 사용자 마일리지 테이블에 넣기
def use_coupon(user_email, coupon_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = "SELECT usepoint FROM mileage_category where id = %s"
            cursor.execute(sql, (coupon_id,))
            result = cursor.fetchall()
            use_point = result[0]['usepoint']
            con.commit()

        with connect(**connectionString) as con:
            cursor = con.cursor()

            mileage_before_sql = "SELECT mileage FROM user WHERE email = %s"
            cursor.execute(mileage_before_sql, (user_email,))
            result = cursor.fetchall()
            con.commit()
            mileage_before = result[0]['mileage']
            mileage_after = mileage_before - use_point

            sql = "UPDATE user SET mileage = mileage - %s WHERE email = %s"
            cursor.execute(sql, (use_point, user_email))
            cursor.fetchone()
            con.commit()

            affected_rows = cursor.rowcount
            if affected_rows > 0:
                kst = pytz.timezone('Asia/Seoul')
                current_date = datetime.now(kst).strftime('%Y-%m-%d')
                mileage_tracking_sql = "INSERT INTO mileage_tracking (user_email, mileage_category_id, before_mileage, after_mileage, use_date) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(mileage_tracking_sql, (user_email, coupon_id, mileage_before, mileage_after, current_date))
                con.commit()
                
                expiration_date = (datetime.now(kst) + timedelta(days=30)).strftime('%Y-%m-%d')
                coupon_list_sql = "INSERT INTO coupon_list (expired_date, user_email, mileage_category_id) VALUES (%s, %s, %s)"
                cursor.execute(coupon_list_sql, (expiration_date, user_email, coupon_id))
                con.commit()
                return mileage_after
    except Exception as e:
        app.logger.debug(e)
        return 500


def use_donation(user_email, donation_id):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT usepoint FROM mileage_category where id = %s"
            cursor.execute(sql, (donation_id,))
            result = cursor.fetchall()
            use_point = result[0]['usepoint']
            con.commit()
        with connect(**connectionString) as con:
            cursor = con.cursor()
            mileage_before_sql = "SELECT mileage FROM user WHERE email = %s"
            cursor.execute(mileage_before_sql, (user_email,))
            result = cursor.fetchall()
            con.commit()
            mileage_before = result[0]['mileage']
            mileage_after = mileage_before - use_point

            sql = "UPDATE user SET mileage = mileage - %s WHERE email = %s"
            cursor.execute(sql, (use_point, user_email))
            cursor.fetchone()
            con.commit()
            affected_rows = cursor.rowcount
            if affected_rows > 0:
                kst = pytz.timezone('Asia/Seoul')
                current_date = datetime.now(kst).strftime('%Y-%m-%d')
                mileage_tracking_sql = "INSERT INTO mileage_tracking (user_email, mileage_category_id, before_mileage, after_mileage, use_date) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(mileage_tracking_sql, (user_email, donation_id, mileage_before, mileage_after, current_date))
                con.commit()
                return mileage_after
    except Exception as e:
        app.logger.debug(e)
        return 500


# 사용자 현재 마일리지 잔액 가져오기
def get_user_mileage(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = "SELECT mileage FROM user where email = %s"
            cursor.execute(sql, (user_email,))
            user_mileage = cursor.fetchone()['mileage']

            return user_mileage

    except Exception as e:
        app.logger.debug(e)


def get_tracking(user_email, start_date, end_date):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            select_sql = ("SELECT mt.*, mc.* FROM mileage_tracking mt JOIN mileage_category mc "
                          "ON mt.mileage_category_id = mc.id "
                          "WHERE mt.use_date BETWEEN %s AND %s AND mt.user_email = %s AND mc.id != 1 "
                          "ORDER BY mt.use_date DESC")
            cursor.execute(select_sql, (start_date, end_date, user_email))

            result = cursor.fetchall()
            combined_result = []

            for row in result:
                combined_row = {
                    "id": row['id'],
                    "use_date": row['use_date'].strftime('%Y-%m-%d'),
                    "user_email": row['user_email'],
                    "mileage_category_id": row['mileage_category_id'],
                    "before_mileage": row['before_mileage'],
                    "after_mileage": row['after_mileage'],
                    "mileage_category": {
                        "id": row['id'],
                        "name": row['name'],
                        "usepoint": row['usepoint'],
                        "category": row['category']
                    }
                }
                combined_result.append(combined_row)

            app.logger.debug(combined_result)
            return combined_result

    except Exception as e:
        app.logger.debug(e)
        return None


def get_all_tracking(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            select_sql = ("SELECT mt.*, mc.* FROM mileage_tracking mt JOIN mileage_category mc "
                          "ON mt.mileage_category_id = mc.id "
                          "WHERE mt.user_email = %s AND mc.id != 1 "
                          "ORDER BY mt.use_date DESC")
            cursor.execute(select_sql, (user_email))

            result = cursor.fetchall()
            combined_result = []

            for row in result:
                combined_row = {
                    "id": row['id'],
                    "use_date": row['use_date'].strftime('%Y-%m-%d'),
                    "user_email": row['user_email'],
                    "mileage_category_id": row['mileage_category_id'],
                    "before_mileage": row['before_mileage'],
                    "after_mileage": row['after_mileage'],
                    "mileage_category": {
                        "id": row['id'],
                        "name": row['name'],
                        "usepoint": row['usepoint'],
                        "category": row['category']
                    }
                }
                combined_result.append(combined_row)

            app.logger.debug(combined_result)
            return combined_result

    except Exception as e:
        app.logger.debug(e)
        return None
# 사용자 현재 마일리지 잔액 가져오기
def get_user_mielage(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = "SELECT mileage FROM user where email = %s"
            cursor.execute(sql, (user_email,))
            user_mileage = cursor.fetchone()['mileage']

            return user_mileage

    except Exception as e:
        app.logger.debug(e)


# AI 판독 성공 후 마일리지 적립
def add_mileage(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = "UPDATE user SET mileage = mileage + 100 WHERE email = %s"
            cursor.execute(sql, (user_email, ))
            con.commit()

            select_sql = "SELECT mileage FROM user WHERE email = %s"
            cursor.execute(select_sql, (user_email,))
            updated_mileage = cursor.fetchone()['mileage']
            
            
            # Insert a record into mileage_tracking
            kst = pytz.timezone('Asia/Seoul')
            current_date = datetime.now(kst).strftime('%Y-%m-%d')
            insert_tracking_sql = "INSERT INTO mileage_tracking (user_email, mileage_category_id, before_mileage, after_mileage, use_date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_tracking_sql, (user_email, 1, updated_mileage-100, updated_mileage, current_date))
            con.commit()

            return updated_mileage

    except Exception as e:
        app.logger.debug(e)


def get_mileage_count(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = "SELECT COUNT(*) as mileage_count FROM mileage_tracking WHERE user_email = %s AND mileage_category_id = 1"
            cursor.execute(sql, (user_email,))
            mileage_count = cursor.fetchone()['mileage_count']

            return mileage_count

    except Exception as e:
        app.logger.debug(e)
        return 0

def get_donation_count(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = ("SELECT COUNT(*) as donation_count "
                   "FROM mileage_tracking mt "
                   "JOIN mileage_category mc ON mt.mileage_category_id = mc.id "
                   "WHERE mt.user_email = %s AND mc.category = 'donation'")
            
            cursor.execute(sql, (user_email,))
            donation_count = cursor.fetchone()['donation_count']
            return donation_count

    except Exception as e:
        app.logger.debug(e)
        return 0


def get_mileage_grade(user_email):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            sql = ("SELECT COUNT(*) as grade "
                   "FROM mileage_tracking "
                   "WHERE user_email = %s AND mileage_category_id = 1")
            
            cursor.execute(sql, (user_email,))
            grade = cursor.fetchone()['grade']
            
            return grade

    except Exception as e:
        app.logger.debug(e)
        return 0
