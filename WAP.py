
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

def load_output():
    df = pd.read_excel("Output.xlsx")
    for key, value in df.iteritems():
        # print("~~~~~~~~~~~~~~~")
        # print(type(value))
        # print()
        update_final(value.list())

def save_output():
    df = pd.DataFrame(Final_List_Of_DATA_Lists)
    print("saving")
    df.to_excel("Output.xlsx")

def load_driver_and_webpage():
    driver = webdriver.Chrome()
    driver.get('http://web.whatsapp.com')
    print('Please Scan the QR Code')
    print("Execute next cell after 10 seconds")
    return driver

def get_full_contactbox_info(contact_box):
    temp = contact_box.find_element_by_class_name("_3H4MS")
    cnt = str(temp.text)
    temp = contact_box.find_element_by_class_name("_1Wn_k")
    fst_msg_box = str(temp.text)

    thisdict = {
        "contact": cnt,
        "msg_preview": fst_msg_box,
    }
    return thisdict

def get_exact_contact_name_from_chat(chat_box):
    return chat_box.find_element_by_class_name("_19vo_").text

def clutfree(chat):
    remove_list = ['MONDAY',
                   'TUESDAY',
                   'WEDNESDAY',
                   'THURSDAY',
                   'FRIDAY',
                   'SATURDAY',
                   'SUNDAY',
                   'YESTERDAY',
                   'TODAY',
                   'UNREAD MESSAGE']

    final_list = []
    for word in chat:
        str = ""
        str += word
        if (str not in remove_list):
            if ((str.endswith(' AM') or str.endswith(' PM')) != True):
               final_list.append(str)
    return final_list

def get_full_chatbox_info(chat_box):
    phone_nums = ""
    email_ids = ""
    messages = ""
    rawchatdata = (
        (chat_box.find_element_by_class_name("_1ays2")).text).split("\n")
    contact_chatlist = clutfree(rawchatdata)
    for chats in reversed(contact_chatlist):
        for matched in phonenumbers.PhoneNumberMatcher(chats, "IN"):
            phone_nums += str(matched.number)
            phone_nums += '\n'
        try:
            v = validate_email(chats)  # validate and get info
            email_ids += str(v["email"])  # replace with normalized form
            email_ids += '\n'
        except:  # EmailNotValidError as e:
            continue
    listlen = len(contact_chatlist)
    if listlen <= 10:
        messages = '\n'.join(contact_chatlist)
    elif listlen > 10:
        messages = '\n'.join(contact_chatlist[-10:])
    chatdict = {
        "phone_numbers": phone_nums,
        "email_ids": email_ids,
        "messages": messages,
    }
    return chatdict
def update_final(ls):
    if ls[0] not in Final_Names_Set:
        Final_Names_Set.add(ls[0]) # Adding name to set for uniqueness
        Final_List_Of_DATA_Lists.append(ls)
print('Functions Loaded')

# %% # (3
driver = load_driver_and_webpage()



#%% 
if True: # Refresh
    time.sleep(1)
    driver.refresh()
    contacts_name_set = set() ### Set of all contacts (Unique String Elements), left tab
    contacts_list = list() ### All scrapped names from contact selection, left tab
    chatbox_name_set = set() ### Set of all contacts (Unique String Elements), Right tab
    contacts_name_set.add('Sunil')
    Final_Names_Set = set()
    Final_List_Of_DATA_Lists = []
    Final_List_Of_DATA_Lists.append(['Name', 'Phone Number', 'Email IDs','Last 10 Messages'     ])
    Final_List_Of_DATA_Lists.append(['Sunil', '9555776578', 'imsunilkj@gmail.com','Hello World'     ])
    current_contact_selected = None ### Currently selected contact while execution #May be unnecessary  
    tab_left_indexes = None
    tab_right_indexes = None
    name_to_add = None
    full_chatbox_info = None

# %%

runlimit = 35
milli_sec = 100
milli_sec = milli_sec / 1000

for i in range(runlimit):
    already_waited = False
    tab_left_indexes = driver.find_elements_by_class_name("X7YrQ")
    tab_right_indexes = driver.find_elements_by_class_name("NuujD")
    for name in tab_left_indexes:
                ### Getting all data from contact box
                try:
                    contact_details = get_full_contactbox_info(name)
                except:
                    print("Error getting contact")
                    pass
                # Checking duplicate contact with string set
                if str(contact_details.get("contact")) not in contacts_name_set:
                    ### Backing up all contact dictionaries
                    contacts_name_set.add(str(contact_details.get("contact")))
                    contacts_list.append(contact_details)
    for chat_box in tab_right_indexes:
            ### 2) Getting contact name again(For verification) and chatbox
            ### Scraping exact contact(name or number) from chat_box
            ls = list()
            try:
                current_contact_selected = get_exact_contact_name_from_chat(chat_box)
            except:
                # print("Error getting selected contact")
                pass
            
            # Checking duplicate contact from chatbox with string set
            if current_contact_selected not in chatbox_name_set:
                # print(current_contact_selected) # FIXME printing
                chatbox_name_set.add(str(current_contact_selected))
            
            ### 3) Getting chat from selected box
            ### Will received this dictionary by get_full_chatbox_info()
            ### Getting full selected chat box data
            get_chat = False
            count = 0 
            for i in range(3):
                try:
                    full_chatbox_info = get_full_chatbox_info(chat_box)
                except:
                    # print("Error in selected contact chat, Waiting...")
                    time.sleep(milli_sec)
                    pass
            
            ### Checking if received final data or not
            # if yes, Will add all data to final data
            #  The final verification to add the final info is 
            # (left Contact name + Msg Preview )
            # Right(Contact name + msg preview from chats)
            
            # Checking Left conditions
            # To check current contact we have to verify with 
            if current_contact_selected in contacts_name_set:
                # Now traversing contacts_list 
                for i in range(len(contacts_list)):
                    # Checking for contact name in chat box
                    if contacts_list[i].get("contact") == current_contact_selected:
                        # Verifiying if message previes available in selected contact chat
                         if contacts_list[i].get("msg_preview") in full_chatbox_info.get("messages").split("\n"):
                            # Adding contact to final List
                            # ['Name', 'Phone Number', 'Email IDs','Last 10 Messages']
                            ls = [current_contact_selected,
                                  full_chatbox_info.get("phone_numbers"),
                                  full_chatbox_info.get('email_ids'),
                                  full_chatbox_info.get('messages')]
                            update_final(ls)
    
    if i%5 == 0:
        save_output()
        print(i, "Saved")
    i = i + 1
    if already_waited == False:
        time.sleep(milli_sec)
    print("Ran for ", i, " Time", len(contacts_name_set), len(chatbox_name_set))


#%%
print()
get_full_contactbox_info(driver.find_elements_by_class_name("X7YrQ"))
