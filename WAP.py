
# %%
### Imports ### (1
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from email_validator import validate_email, EmailNotValidError
from phonenumbers import carrier
import time
import phonenumbers
import datetime
import pandas as pd
print("### Packages Imported ###")
print(datetime.datetime.now())

# %% # (2)

def pandu():
    df = pd.DataFrame(index='Phone Numbers', columns=['Name', 'Phone Numbers', 'Email Ids', 'Last Messages'])
    df.append(['Sunil',
              9555776578,
              'imsunilkj@gmail.com',
              'Hi Hello How are you'],
              columns=list('Name',
                           'Phone Numbers',
                           'Email Ids',
                           'Last Messages'))

    # df.append(['Sunil',
    #           9555776578,
    #           'imsunilkj@gmail.com',
    #           'Hi Hello How are you'],
    #           columns=list('Name',
    #                        'Phone Numbers',
    #                        'Email Ids',
    #                        'Last Messages'))
    # df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
    print(df)
    print('Hello')
    # pandu()
##########################################################
### Defined Functions ####################################
##########################################################
def load_driver_and_webpage():
    ### Loading chrome in web driver and Opening webpage ###
    driver = webdriver.Chrome()
    driver.get('http://web.whatsapp.com')
    ### Waiting for QR Code to be scanned ###
    print('Please Scan the QR Code')
    print("Execute next cell after 10 seconds")
    ### Web page should be opened up and ready for further execution ###
    return driver
    ### Web page should be opened up and ready for further execution ###
##########################################################
def get_full_contactbox_info(contact_box):
    ### Details is information dictionary to return
    ### Getting exact contact by CSS
    temp = contact_box.find_element_by_class_name("_3H4MS")
    cnt = str(temp.text)
    ### Getting first message preview from contact box - _1Wn_k _19RFN _1ovWX _F7Vk
    temp = contact_box.find_element_by_class_name("_1Wn_k")
    fst_msg_box = str(temp.text)

    thisdict = {
        "contact": cnt,
        "msg_preview": fst_msg_box,
    }
    return thisdict
##########################################################

def get_exact_contact_name_from_chat(chat_box):
    ### Getting exact contact name with _19vo_
    return chat_box.find_element_by_class_name("_19vo_").text
##########################################################

def clutfree(chat):
    ### Words to remove ###
    days = """MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY SUNDAY YESTERDAY TODAY"""
    ### Converted to list and added words###
    remove_list = days.split(' ')
    remove_list.append('UNREAD MESSAGE')  # Appedded 'UNREAD MESSAGE'

    final_list = []
    for word in chat:
        # For loop
        str = ""
        str += word
        # or (str.endswith(' AM') or str.endswith(' PM')) :
        if (str not in remove_list):
            # print(str)
            if ((str.endswith(' AM') or str.endswith(' PM')) != True):
               final_list.append(str)
    return final_list
##########################################################

def get_full_chatbox_info(chat_box):
    phone_nums = ""
    email_ids = ""
    messages = ""
    ### Getting full chat with _1ays2 ###
    rawchatdata = (
        (chat_box.find_element_by_class_name("_1ays2")).text).split("\n")
    ### Cleaning chat ###
    contact_chatlist = clutfree(rawchatdata)
    ### Running loop on last 5 text messages
    ### Reverse loop of contact_chatlist
    for chats in reversed(contact_chatlist):
        ### Trying to get phone number from chat
        for matched in phonenumbers.PhoneNumberMatcher(chats, "IN"):
            phone_nums += str(matched.number)
            phone_nums += '\n'
        # print(phone_nums)
        ### Getting all email addresses
        try:
            v = validate_email(chats)  # validate and get info
            email_ids += str(v["email"])  # replace with normalized form
            email_ids += '\n'
            # print(email_ids)
        except:  # EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            # print(str(e))
            continue
    ### Addind last 10 strings, Dont know how
    listlen = len(contact_chatlist)
    if listlen <= 10:
        messages = '\n'.join(contact_chatlist)
        # last_messages = contact_chatlist.copy()
        # messages = '\n'.join(last_messages)

    elif listlen > 10:
        # last_messages = contact_chatlist[-5:]
        messages = '\n'.join(contact_chatlist[-10:])

    # messages = '\n'.join(last_messages)
    # print(messages)

    chatdict = {
        "phone_numbers": phone_nums,
        "email_ids": email_ids,
        "messages": messages,
    }
    # temp = get_full_chatbox_info(chat_box)
    # print(temp)
    # return chatdict
    return chatdict
##########################################################
print('Functions Loaded')
##########################################################
##########################################################

# %% # (3

##########################################################
### Final Execution ######################################
##########################################################
driver = load_driver_and_webpage()
##########################################################

#%% ######################################################
### Refreash Page and Variables ### Optional
##########################################################
time.sleep(1)
driver.refresh()
### Final Data and Constructor behaviour ###
### Left Box, All Contacts
contacts_name_set = set() ### Set of all contacts (Unique String Elements), left tab
contacts_dict_list = list() ### All scrapped names from contact selection, left tab
### Right Box, Selected Contact & Respective Chat
chatbox_name_set = set() ### Set of all contacts (Unique String Elements), Right tab
chat_contactswise_list = list() ### All scrapped names from selection contact, Right tab
Final_List_Of_DATA_Lists = list()
current_contact_selected = None ### Currently selected contact while execution #May be unnecessary  

tab_left_indexes = None
tab_right_indexes = None
name_to_add = None
full_chatbox_info = None
# FIXME this df is for final result
# dataframe = pd.DataFrame(columns=['Name', 'Phone Numbers', 'Email Ids', 'Last Messages'], ignore_index=True)
##########################################################

# %%
### Final Execution ### Webpage3 should be ready, last Execution
##########################################################
### Repeating further code till runlimit with a delay of wait_time, wait_time is in millisecs
##########################################################
runlimit = 10
milli_sec = 50
milli_sec = milli_sec / 1000

for i in range(runlimit):
        already_waited = False
        ##########################################################
        ##########################################################
        ### Got Both, 1) Allcontact boxes, 2)Chat box
        tab_left_indexes = driver.find_elements_by_class_name("X7YrQ")
        tab_right_indexes = driver.find_elements_by_class_name("NuujD")
        ##########################################################
        ### Getting contact(name or number) in string
        for name in tab_left_indexes:
                ### Getting all data from contact box
                contact_details = get_full_contactbox_info(name)
                if contact_details != None:
                    # print(contact_details.get("contact"))
                    ### Backing up all contact dictionaries
                    contacts_dict_list.append(contact_details)
                    contacts_name_set.add(contact_details.get("contact"))
                    ### All data is stored in two data sets-> contacts_dict_list, contacts_name_set
            # try:
                
            # except:
            #     print('### Error on Left, Waiting... ###')
            #     time.sleep(milli_sec)
            #     already_waited = True
        ##########################################################

        for chat_box in tab_right_indexes:
            ls = list()
                ### Getting contact name again(For verification) and chats
                ### Scraping exact contact(name or number) from chat_box
            current_contact_selected = get_exact_contact_name_from_chat(chat_box)
            if current_contact_selected != None:
                print(current_contact_selected)
                chatbox_name_set.add(str(current_contact_selected))
                    ### Getting chat from selected box
                    ### Will received this dictionary by get_full_chatbox_info()
                ### Getting full selected chat box data
            full_chatbox_info = get_full_chatbox_info(chat_box)
            try:
                #  print(full_chatbox_info.get('phone_numbers'),full_chatbox_info.get('email_ids'),full_chatbox_info.get('messages'))
                ### Checking if received final data or not
                #   if yes, Will add all data to final data 
                if full_chatbox_info != None:
                    ### Adding data to final sheet
                    name_to_add = chatbox_name_set.pop() 
                    ### Adding to list
                    ls.append(name_to_add)
                    ls.append(full_chatbox_info.get('phone_numbers'))
                    ls.append(full_chatbox_info.get('email_ids'))
                    ls.append(full_chatbox_info.get('messages'))
                    ### Adding again to contact set
                    chatbox_name_set.add(name_to_add)
                    ### Backing up data
                    chat_contactswise_list.append(full_chatbox_info)
                    # print(ls)
                    # ls = None
                    
                    
                    ### Adding to final list

                    if contacts_name_set.intersection(set(name_to_add)) != Final_List_Of_DATA_Lists[-1][0]:
                        Final_List_Of_DATA_Lists.append(ls)
                        print(Final_List_Of_DATA_Lists[-1])
                        # print(ls)
            except:
                print('### Error on right, Waiting... ###')
                time.sleep(milli_sec)
                already_waited = True
            
    
                
        ##########################################################
        ##########################################################
            # dataframe.append({
            #         'Name': 'suniol',
            #         'Phone Numbers': full_chatbox_info.get('phone_numbers'),
            #         'Email Ids': full_chatbox_info.get('email_ids'),
            #         'Last Messages': full_chatbox_info.get('messages')
            #         })
        ####################
        ### Analyse Here ### TODO
        ####################
        i = i + 1
        if already_waited == False:
            time.sleep(milli_sec)
        ### Completed ############################################
        ##########################################################
        print("Ran for ", i, " Time", len(contacts_name_set), len(chatbox_name_set))
# print(Final_List_Of_DATA_Lists)
# print('~~~',chatbox_name_set)
# print('\n','\n')
# print("Final Testing Output"," -> ", "Contacts names set")
# print(contacts_name_set)
# dataframe.tail[1]

# %% # chatbox_name_set , chat_contactswise_list
# chatdict = {
#         "phone_numbers": phone_nums,
#         "email_ids": email_ids,
#         "messages": messages,}

# for elem in chatbox_name_set:
#     datetime

print(chatbox_name_set)
print()
print(chat_contactswise_list)
get_full_contactbox_info(driver.find_elements_by_class_name("X7YrQ"))

# %%
Final_List_Of_DATA_Lists

# %%
ls

# %%
