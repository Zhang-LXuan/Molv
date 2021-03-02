from .hmmCut import HmmCut
from polls.models import Question
def Question_Match(original_question,question_list,matched_num):
    all_question_list=[]
    for i in question_list:
        all_question_list.append(str(i.question_text))
    cuter=HmmCut()
    result=[]
    list1=cuter.cut(original_question)
    for question in all_question_list:
        list2=cuter.cut(question)
        num=0
        for item in list1:
            if item in list2:
                num+=1
        result.append(num)
    result_dict=dict(zip(all_question_list,result))
    result_list = sorted(result_dict.items(),key = lambda x:x[1],reverse = True)
    result=[]
    for item in range(matched_num):
        for i in question_list:
            if i.question_text==result_list[item][0]:
                result.append(i)
                i.matched_nums+=1
                i.save()
                break
    return result