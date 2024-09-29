from splitwise import Expense, Splitwise
from splitwise.expense import ExpenseUser
# get these values from here https://secure.splitwise.com/apps
from dotenv import load_dotenv
import os
load_dotenv()

cus_key = os.getenv('cus_key')
cus_secret = os.getenv('cus_secret')
api_key = os.getenv('api_key')

sObj = Splitwise(cus_key ,cus_secret , api_key=api_key)

print(f"Hello {sObj.getCurrentUser().first_name} {sObj.getCurrentUser().last_name}")

expenses_to_add = [
                    
                    
                    ("Publix", 37.14, ("ALL")),
                    ]
Group_ID = None
for grp in sObj.getGroups():
    if grp.getName() == "Mainu-Tainu":
        Group_ID = grp.getId()
# Group_ID = next(grp.getId() for grp in sObj.getGroups() if grp.getName() == "Mainu-Tainu")
assert Group_ID is not None, "Group ID not found"
users_map = {}
for user in sObj.getGroup(Group_ID).getMembers():
    users_map[user.getFirstName().lower()] = user

for exp in expenses_to_add:
    splitwise_exp  = Expense()
    splitwise_exp.setCurrencyCode("USD")
    splitwise_exp.setDescription(f"{exp[0]}")
    splitwise_exp.setCost(exp[1])
    splitwise_exp.setGroupId(Group_ID)
    if "ALL" in exp[2]:
        splitwise_exp.setSplitEqually()
    else:
        gaurav = users_map["gaurav"]
        me = ExpenseUser()
        me.setId(gaurav.getId())
        me.setOwedShare(exp[1]/2)
        me.setPaidShare(exp[1])
        other = ExpenseUser()
        other.setOwedShare(exp[1]/2)
        if "ritesh" in exp[2]:
            ritesh = users_map["ritesh"]
            other.setId(ritesh.getId())
        else:
            nidhima = users_map["nidhima"]
            other.setId(nidhima.getId())
        splitwise_exp.addUser(me)
        splitwise_exp.addUser(other)
            
    print(exp)
    
    nExpense, errors = sObj.createExpense(splitwise_exp)
    if errors:
        print(f"Failed to add expense {exp} with {errors.getErrors()}")
