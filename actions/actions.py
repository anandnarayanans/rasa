
import json
import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# from rasa.core.actions import Action
# from .mongo import mongo_connector



#write python code for fetching mongodb employee collection data and display in rasa chatbot
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted



class ActionEmployee(Action):
    
    def name(self):
        return "action_fetch_employee"
   
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            client = MongoClient("mongodb+srv://hari:hari@cluster0.3xr0vsj.mongodb.net/")
            db = client['Demo']
            collection = db['rasa']

            data = collection.find()
            
        #     #extract emplyee name,department and job title and display in rasa chatbot
            
            employees = []
            for document in data:
                employees.append({
                    "name": document["name"],
                    "department": document["department"],
                    "job_title": document["job_title"],
                    "salary": document["salary"]
                })
                
            message = "\n".join(f"- Name: {employee['name']} Department: {employee['department']} Job Title: {employee['job_title']} Salary: {employee['salary']}" for employee in employees)
           
            dispatcher.utter_message(text=message)
            
            

        #     # Extract specific data from documents
        #     # employees = []
        #     # for document in data:
        #     #     employees.append({
        #     #         "name": document["name"],
        #     #         "department": document["department"],
        #     #     })

        #     # # Build and send message with extracted data
        #     # message = "\n".join(f"- {employee['name']} ({employee['department']})" for employee in employees)
        #     # dispatcher.utter_message(text=message)
        except Exception as e:
            logging.error(f"Error fetching employee data: {e}")
            dispatcher.utter_message(text="Sorry, I couldn't find any employee information.")

        return []
    
   



class ActionEmployeeID(Action):
    
    def name(self):
        return "action_fetch_employee_id"
   
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        client = MongoClient("mongodb+srv://hari:hari@cluster0.3xr0vsj.mongodb.net/")
        db = client['Demo']
        collection = db['rasa']

        data = collection.find()


        employee_id = tracker.get_slot("employee_id")
        print(type(employee_id))
        
        #convert string to int
        employee_id = int(employee_id)
        
        print(employee_id)
        document = collection.find_one({"id": employee_id})
        print(document)
        # Build and send the formatted message
        if document:
            message = f"**Employee Details:**\n" \
                        f"- ID: {document['id']}\n" \
                        f"- Name: {document['name']}\n" \
                        f"- Department: {document['department']}\n" \
                        f"- Job Title: {document['job_title']}\n" \
                        f"- Salary: ${document['salary']:,}"
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Sorry, couldn't find the employee. Please try again.")

        return []
