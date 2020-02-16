temp = ['TUESDAY', '11:52 PM', 'Ok', '11:53 PM', 'Haa jaipur kar lijo',
         '11:53 PM', 'Sbse paas station konso h?', '11:53 PM', 
         'Ksr Ya yasvantpur ?', '11:53 PM', 'Dono same he hai', 
         '11:54 PM', 'Ya or koi', '11:54 PM', 'Ksr kar le', 
         '11:54 PM', 'M ji station se gyo ho coimbatore', 
         '11:54 PM', 'Biko naam yaad h?', '11:54 PM', 
         'Ksr kar leee', '11:54 PM', 'Bado station hai', 
         '11:54 PM', 'Okii', '11:54 PM', 'Yaad bhi koni', 
         '11:55 PM', 'Oki oki', '11:55 PM', '11:55 PM', 
         'WEDNESDAY', 'Ut gyo ki?', '4:15 PM', 'Haa utodo huuu', 
         '4:34 PM', 'YESTERDAY', 'Uut gyo?', '3:43 PM', 'Haaa g', 
         '5:21 PM']
def clutfree(chat):
    ### Words to remove ###
    days = """MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY SUNDAY YESTERDAY TODAY"""
        
    ### Converted to list and added words###
    remove_list = days.split(' ')
    remove_list.append('AM') # Appedded AM
    remove_list.append('PM') # Appedded PM
    remove_list.append('UNREAD MESSAGE') # Appedded 'UNREAD MESSAGE'
    
    final_list = []
    for i in range(len(chat)):
        for j in range(len(remove_list)):
            if remove_list[j] in chat[i]:
                print(chat[i])
            else:    
                final_list.append(j)

    # print(delete_list)
    # for i in range(len(delete_list)):
    #      chat.pop(int(delete_list[i]))
    print(final_list)

    return final_list
    
clutfree(temp)