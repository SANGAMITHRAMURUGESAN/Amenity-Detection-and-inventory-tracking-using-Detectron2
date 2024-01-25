from Detector import *
import streamlit as st
from PIL import Image
from collections import Counter
import dbconnect
def detection():
    # st.title('Airbnb Object Detection and Inventory Management')
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0
    if "item_counts" not in st.session_state:
        st.session_state["item_counts"] = {}

    st.header('Please upload an image')
    image_file = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'],key=st.session_state["file_uploader_key"],)
    if image_file is not None:
        st.session_state["file_uploader_key"] += 1
        detector = Detector()
        newsize = (320, 320)
        with open(image_file.name, mode="wb") as f:
            f.write(image_file.getbuffer())
        listofitems = detector.onImage(image_file.name)
        img_ = Image.open("result.jpg")
        img_ = img_.resize(newsize)
        st.image(img_, caption='Processed Image.')
        item_counts = {}
        for item in listofitems:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1

        for key, value in item_counts.items():
            if key in st.session_state["item_counts"]:
                st.session_state["item_counts"][key] += value
            else:
                st.session_state["item_counts"][key] = value

    if st.button("Clear uploaded files"):
        st.session_state["file_uploader_key"] += 1
        #st.session_state["item_counts"] = {}
        st.experimental_rerun()
    return st.session_state["item_counts"]

def check_lists(df1, addressid):
    side_1, side_2, side_3 = st.columns(3)
    with side_1:
        st.write('available amenities')
        available = df1[df1["ADDRESSID"] == addressid][['amenityname', 'quantity']]
        st.session_state["available"] = dict(zip(available['amenityname'], available['quantity']))
        for index, item in available.iterrows():
            # st.checkbox(str(item["quantity"]) + " " + str(item['amenityname']), key="available-" + item['amenityname'])
            st.markdown("- " + str(item["quantity"]) + " " + str(item['amenityname']))
        st.write()

    with side_2:
        if st.session_state["item_counts"] == {}:
            mydb = dbconnect.connect_db()
            cursor = mydb.cursor()
            cursor.execute(
                "SELECT A.AMENITYNAME, COUNT FROM AMENITY A, USER_LIST B, TRANSACTIONS C WHERE A.AMENITYID = C.AMENITYID and B.USERID = C.USERID_HOST and C.ADDRESSID = %s and C.CHANGED_BY ='guest' and B.USERNAME = %s;",
                [addressid,st.session_state['username']])
            #and END_DATE = (SELECT MAX(END_DATE) FROM USER_LIST B, TRANSACTIONS C where C.USERID_HOST and C.ADDRESSID = %s and C.CHANGED_BY is not null and B.USERNAME = %s)
            all = cursor.fetchall()
            items = {item[0]: item[1] for item in all}
            st.session_state["item_counts"] = items
        st.write('detected items')
        for key, value in st.session_state["item_counts"].items():
            st.markdown("- " + str(value) + " " + str(key))

    with side_3:
        st.write('difference')
        st.session_state["difference"]=difference()
        response1 = st.button('update new inventory')
        response2 = st.button('decline new inventory')
        if response1:
            update_inventory(addressid)
            st.write("accepted")
        if response2:
            st.session_state["file_uploader_key"] += 1
            st.session_state["item_counts"] = {}
            st.experimental_rerun()
            st.write("declined")

def update_inventory(addressid):
    username = st.session_state['username']
    item_counts = st.session_state["item_counts"]
    availble = st.session_state["available"]
    mydb = dbconnect.connect_db()
    cursor = mydb.cursor()
    cursor.execute("SELECT USERID FROM USER_LIST WHERE USERNAME = %s;", [username])
    userid = cursor.fetchall()
    st.write(userid[0][0])
    for key, value in st.session_state["difference"].items():
        cursor.execute("SELECT AMENITYID FROM AMENITY WHERE AMENITYNAME = %s;", [key])
        amenityid = cursor.fetchall()
        if key in item_counts and key in availble:
            if value!=0:
                cursor.execute(
                    "UPDATE AMENITIES_LIST SET QUANTITY = %s WHERE USERID = %s and ADDRESSID = %s and AMENITYID= %s",
                    [item_counts[key], userid[0][0], addressid, amenityid[0][0] ])
                cursor.execute("commit;")
        elif key in item_counts and not (key in availble):
            cursor.execute(
                "INSERT INTO AMENITIES_LIST (USERID, ADDRESSID, AMENITYID, QUANTITY) VALUES (%s, %s, %s, %s)",
                [userid[0][0], addressid, amenityid[0][0], value])
            cursor.execute("commit;")
        elif not(key in item_counts) and  key in availble:
            cursor.execute(
                "delete from AMENITIES_LIST where USERID = %s and  ADDRESSID = %s and  AMENITYID=%s",
                [userid[0][0], addressid, amenityid[0][0]])
            cursor.execute("commit;")
    st.experimental_rerun()



   #########   continue from here

def difference():
    # Two example dictionaries
    dict1 = st.session_state["item_counts"]
    dict2 = st.session_state["available"]

    # Get the counts of values for each dictionary
    count1 = Counter(dict1)
    count2 = Counter(dict2)

    # Calculate the difference in counts
    count_difference = {}

    # Subtract counts from dict2
    for key, count in count2.items():
        count_difference[key] = count1.get(key, 0) - count

    # Add counts from dict1 for keys not present in dict2
    for key, count in count1.items():
        if key not in count2:
            count_difference[key] = count
    for key, count in count_difference.items():
        if count <0  :
            st.error(str(count) + " " + str(key))
        else:
            st.success(str(count) + " " + str(key))

    # Display the result
    return count_difference


