def get_full_contactbox_info(contact_box):
    ### Details is information dictionary to return
    # detail = {}
    
    ### Getting exact contact by CSS 
    temp = contact_box.find_element_by_class_name("_3H4MS")
    cnt = str(temp.text) 
    # print(cnt)
    ######

    ### Getting first messge preview from contact box - _1Wn_k _19RFN _1ovWX _F7Vk
    temp = contact_box.find_element_by_class_name("_1Wn_k")
    fst_msg_box = str(temp.text)
    # print(fst_msg_box)

    thisdict = {
    "contact": cnt,
    "msg_preview": fst_msg_box,  
    }
    
    return thisdict
############################################################################################################
############################################################################################################
def get_full_chatbox_info(chat_box):
    ### Getting exact contact name with _3V5x5
    contact_name = chat_box.find_element_by_class_name("_3V5x5")
    name = contact_name.text
    
    ### Getting full chat with _1ays2 ###
    rawchatdata = ((chat_box.find_element_by_class_name("_1ays2")).text).split("\n")
    
    ### Running loop on last 5 text messages 
    ### TODO Doing too
    ### Cleaning chat ###

    chatlist = clutfree(rawchatdata)
    print(temp)
####################################
####################################
# test = driver.find_element_by_class_name("NuujD") 
# contact_details = get_full_chatbox_info(test)

############################################################################################################
############################################################################################################

