import json
import datetime
from typing import List, Dict, Union, Optional
from urllib.parse import unquote_plus
from dateutil.parser import parse
import asyncio

import motor.motor_asyncio
from bson.objectid import ObjectId

from email_validator import validate_email, EmailNotValidError
import re

import random

import os 
from dotenv import load_dotenv


###################### mongodb set up ##############################
load_dotenv()
MONGOURI = os.getenv("MONGOURI")
db = motor.motor_asyncio.AsyncIOMotorClient(MONGOURI).spacebase


async def get_meme_record(keywords: list) -> Dict:
    print(keywords)
    query = {
        "$or": [
            {"keywords": {"$in": keywords}},  # match any keyword in the keywords array
            {"description": {"$regex": '|'.join(keywords), "$options" :'i'}}  # match any keyword in the description string
        ]
    }
    
    memes = await db.memes.find(query).to_list(None)

    # Define the count_matches function
    def count_matches(meme):
        match_count = sum(keyword in meme.get('keywords', []) for keyword in keywords)
        match_count += sum(keyword in meme.get('description', '').lower() for keyword in keywords)
        return match_count

    # Sort the memes by the count of matches
    sorted_results = sorted(memes, key=count_matches, reverse=True)

    return {"response": sorted_results}

async def create_meme_record(link:str, description: str, keywords: list, user: dict):

    user = await get_user_record_util_user_info(user)

    if not user:
        return {"error": "User not found. User must be registered to be able to use meme database"}

    # Search for a record with the provided link
    existing_record = await db.memes.find_one({'link': link})

    if existing_record:
        # If the record already exists, return a response indicating so
        return {"error": "Record already exists. Feel free to adjust the current existing record!"}
    else:
        # If no record exists, create a new project from the template
        new_project = {}
        new_project['description'] = description
        new_project['entry_record']= [{"user": user['_id'], "keywords": keywords }]
        new_project['link'] = link
        new_project['created_by'] = user['_id']
        new_project['keywords'] = keywords
        insert_result = await db.memes.insert_one(new_project)
        return {"response": insert_result}


async def update_meme_record(link:str, description: str, keywords: list, user: dict):

    user = await get_user_record_util_user_info(user)

    if not user:
        return {"error": "User not found. User must be registered to be able to use meme database"}

    # Search for a record with the provided link
    existing_record = await db.memes.find_one({'link': link})

    if existing_record:
        # If the record exists, append new description to the existing one
        updated_description = existing_record['description'] + " | " + str(description)
        
        # Add new keywords to the existing list, remove duplicates
        updated_keywords = list(set(existing_record['keywords'] + keywords))
        
        # Update the entry record
        if 'entry_record' in existing_record:
            existing_record['entry_record'].append({"user": user['_id'], "keywords": keywords })
        else:
            existing_record['entry_record'] = [{"user": user['_id'], "keywords": keywords }]

        # Now perform the update
        update_result = await db.memes.update_one(
            {'link': link}, 
            {'$set': 
                {
                    'description': updated_description, 
                    'keywords': updated_keywords,
                    'entry_record': existing_record['entry_record']
                }
            }
        )
        return {"response": "Record Updated"}
    else:
        # If the record doesn't exist, return a response indicating so
        return {"response": "Record not found"}



###################### base code ##############################

def project_base():
    boiler_project = {
        "client": "",
        "worker": None,
        "past_workers": [],
        "created_by": None,
        "description": "",
        "payment": 0,
        "start_date": None,
        "end_date": None, # End date is the date the project needs to be finished
        "due_date": None,
        "init_values": [],
        "updates": [], # {project_percentage, update_datetime, update_message}
        "status": "not_started",  # Options: draft, not_started, in_progress, awaiting_review, in_review, completed
        "ruleset_id": None,
        "review_required": True,
        "timeframe": { # Timeframe to get the project done when started
            "days": 0,
            "hours": 0,
            "minutes": 0
        },
        "review_timeframe": { # Timeframe to get the project done when started
            "days": 0,
            "hours": 0,
            "minutes": 0
        },
        "reviews": [],
        "review_payment": 0,
        "parent_id": None,  # Track parent project
        "brothers": [], # Projects in which also need to finish in order to cascade
        "children": [],
        "parents": [],
        "submissions" : [],
        "submission_fields": [], # Generally a copy of the ruleset init fields
        "permissions": []
    }
    return boiler_project

def ruleset_base():
    boiler_ruleset = {
        "init_fields": [], #criteria for submission and cascading, {"field_name", "field_type", "field_required", "multiple_submissions"}
        "permissions": [],
        "timeframe": { # Timeframe to get the project done when initalized ( sets the project_end date )
            "days": 0,
            "hours": 0,
            "minutes": 0
        },
        "owner_id": 0,
        "description": "",
        "project_template": project_base(),
        "ruleset_dependents": [] #list of lists
    }
    return boiler_ruleset

def clean_dict(ruleset, keys):
    return {key: ruleset[key] for key in keys if key in ruleset}

def user_base():
    boiler_user = {
        "balance": 0.0,
        "payout_balance": 0.0,
        "credentials": {},
        "email": None,
        "groups": [],
        "discord_id": "",
        "status": {
            "active": True,
            "expected_active": None
        }
    }
    return boiler_user

def permission_base():
    boiler_permissions = {
        "permission_type": "user",
        "permission_id": "",
        "permission": ""
    }
    return boiler_permissions

def group_base():
    boiler_permissions = {
        "users": [],
        "description": ""
    }
    return boiler_permissions

def notification_base():
    boiler_notification = {
        "user_id": "",
        "notification_message": "",
        "notification_status": "unread"
    }
    return boiler_notification

async def get_project_record(project_id: str) -> dict:
    """
    Get a project record given a project_id
    """
    project = await db.projects.find_one({"_id": ObjectId(project_id)})
    return project

async def get_active_projects(user_id: str) -> dict:

    projects = await db.projects.find({"worker": ObjectId(user_id)}).to_list(None)
    return projects

async def get_active_reviews(user_id: str) -> dict:
    active_reviews = await db.projects.find({
        "status": "in_review",
        "reviews": {"$elemMatch": {"worker_id": ObjectId(user_id), "status": "in_progress"}}
        }
    ).to_list(None)
    return active_reviews

async def get_all_user_active_projects_older_than_input(days_old: int) -> list:
    date_threshold = datetime.datetime.utcnow() - datetime.timedelta(days=days_old)
    query = {
        "status": "in_progress",
        "start_date": {"$lte": date_threshold},
        "$expr": {
            "$and": [
                {
                    "$or": [
                        {"$eq": [{"$size": "$updates"}, 0]},
                        {
                            "$lt": [
                                {"$arrayElemAt": ["$updates.update_datetime", -1]},
                                date_threshold
                            ]
                        },
                    ]
                },
                {
                    "$or": [
                        {"$eq": [{"$size": "$submissions"}, 0]},
                        {
                            "$lt": [
                                {"$arrayElemAt": ["$submissions.submission_datetime", -1]},
                                date_threshold
                            ]
                        },
                    ]
                },
                {
                    "$or": [
                        {"$eq": [{"$size": "$reviews"}, 0]},
                        {
                            "$lt": [
                                {"$arrayElemAt": ["$reviews.submission_datetime", -1]},
                                date_threshold
                            ]
                        },
                    ]
                },
            ]
        }
    }

    projects = await db.projects.find(query).to_list(None)
    return projects


async def get_projects(permission_ids: list) -> dict: 
    print(permission_ids)
    projects = await db.projects.find({
        "status": "not_started",
        "permissions": {"$elemMatch": {"permission_id": {"$in": permission_ids}, "permission": "claim"}}
        }
    ).to_list(None)
    return projects

async def get_user_projects(user_id: str) -> List:
    projects = await db.projects.find({
        "client": ObjectId(user_id)
    }).to_list(None)
    return projects

async def get_review_projects(permission_ids: list) -> dict:
    projects = await db.projects.find({
        "status": "awaiting_review",
        "permissions": {"$elemMatch": {"permission_id": {"$in": permission_ids}, "permission": "review"}}
        }
    ).to_list(None)
    return projects

async def get_editable_projects(permission_ids: List) -> Dict:
    projects = await db.projects.find({
        "status": "open",
        "permissions": {"$elemMatch": {"permission_id": {"$in": permission_ids}, "permission": "edit"}}
        }
    ).to_list(None)
    return projects

async def get_ruleset_record(ruleset_id: str) -> Dict:
    ruleset = await db.rulesets.find_one({"_id": ObjectId(ruleset_id)})
    return ruleset

async def get_user_record(user_record: str) -> Dict:
    user = await db.users.find_one({"_id": ObjectId(user_record)})
    return user

async def get_user_record_util_user_info(user_record: Dict) -> Dict:
    user = await db.users.find_one(user_record)
    return user

async def get_user_ruleset_records(user_information: dict) -> List:
    user_record = await get_user_record_util_user_info(user_information)      
    rulesets = await db.rulesets.find({"owner_id": ObjectId(user_record["_id"])}).to_list(None)
    return rulesets

async def get_user_groups(user_id: str):
    users = await db.groups.find({"users": {"$in": [ObjectId(user_id)]}}).to_list(None)
    return users

async def get_group_record(group_id: str):
    users = await db.groups.find({"_id": group_id}).to_list()
    return users

async def get_notifications(user_information: dict) -> List:
    user_record = await get_user_record_util_user_info(user_information)      
    rulesets_cursor = db.notifications.find({"user_id": ObjectId(user_record["_id"])})
    documents = []
    async for document in rulesets_cursor:
        documents.append(document)

    return documents

async def get_platform_notifications(platform: str) -> list:
    if platform == "discord":
        rulesets_cursor = db.discord_notifications.find({"notification_status": "unread"})

        documents = await rulesets_cursor.to_list(length=None)
        if not documents:
            return []

        await db.discord_notifications.update_many(
            {"notification_status": "unread"},
            {"$set": {"notification_status": "read", "notification_opened": datetime.datetime.now()}}
        )

        return documents


async def get_user_permissions(user_dict: dict) -> list:
    group_list = await get_user_groups(str(user_dict["_id"]))

    user_groups = [group['_id'] for group in group_list]
    user_groups.append(user_dict["_id"])

    return user_groups

async def validate_user_permissions(permission_record: dict, user_record: dict, request_permission: str) -> bool:
    user_permissions = await get_user_permissions(user_record)
    for permission in permission_record['permissions']:
        if permission['permission_id'] in user_permissions and permission['permission'] == request_permission:
            return True
    return False


async def create_group_user_notification_records(group_id: str, notification_message: str):
    group_record = await get_group_record(group_id)
    users = group_record['users']

    if not users:
        return {"success": "User(s) not found"}

    for user in users:
        notification_response = await create_user_notification_record(user["_id"], notification_message)
        if "error" in notification_response:
            return {"error": "Something unexpected happened when trying to create a group notification record"}

    return {"success": "Notification(s) created successfully"}

async def create_user_notification_record( user_id: str, notification_message: str):
    new_notification = notification_base()

    new_notification['user_id'] = user_id
    new_notification['notification_message'] = notification_message
    insert_result = await db.notifications.insert_one(new_notification)

    if not insert_result.acknowledged and not insert_result.inserted_id:
        return {"error": "Notification not created"}

    # Create discord notification
    user_record = await get_user_record(user_id)

    if user_record['discord_id'] != "":
        new_notification['user_id'] = user_record['discord_id']
        insert_result = await db.discord_notifications.insert_one(new_notification)

        if not insert_result.acknowledged and not insert_result.inserted_id:
            return {"error": "Notification not created"}

    return {"success": "Notification(s) created successfully"}


async def create_ruleset_record( user_id: str ):
    # Create new ruleset from template
    new_ruleset = ruleset_base()
    new_ruleset["owner_id"] = ObjectId(user_id)
    new_ruleset["project_template"]["client"] = ObjectId(user_id)

    new_permission = permission_base()
    new_permission["permission_id"] = ObjectId(user_id)

    for permission in ["create", "edit", "view", "invite"]:
        new_permission['permission'] = permission
        new_ruleset['permissions'].append(new_permission)

    insert_result = await db.rulesets.insert_one(new_ruleset)

    if insert_result.acknowledged and insert_result.inserted_id:
        return {"success": "Record created successfully with id: {insert_result.inserted_id}"}
    else:
        return {"error": "Record not created"}

def validate_user_info(user_info: Dict[str, str]) -> bool:
    # Validate username
    username_pattern = r'^[a-zA-Z0-9_]{4,20}$'
    if not re.match(username_pattern, user_info.username):
        return {"error": "Username is not a valid username"}

    # Validate password
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%.*?&])[A-Za-z\d@$!%.*?&]{8,}$'
    if not re.match(password_pattern, user_info.password):
        return {"error": "Password is invalid"}

    # Validate email
    try:
        v = validate_email(user_info.email)
    except EmailNotValidError as e:
        return {"error": "Email is not a valid email"}

    # If discord_id is provided, validate it
    if 'discord_id' in user_info and user_info['discord_id']:
        discord_id_pattern = r'^\d{18}$'
        if not re.match(discord_id_pattern, user_info['discord_id']):
            return {"error": "Discord_id is invalid"}

    return {"success": "user_info successfully validated"}

async def create_user_record( user_info: dict = None ):
    # Create base user dict
    new_user = user_base()
    if user_info:
        new_user.update(user_info)

    insert_result = await db.users.insert_one(new_user)

    if insert_result.acknowledged and insert_result.inserted_id:
        return {"success": "Record created successfully with id: {insert_result.inserted_id}"}
    else:
        return {"error": "Record not created"}

async def create_user(user_information: dict) -> dict:

    # Validate submission
    user_info_validation = validate_user_info(user_information)
    if "error" in user_info_validation:
        return {"error": user_info_validation['error']}

    # Validate uniqueness of username
    user_record = await get_user_record_util_user_info({'username': user_information.username})
    if user_record:
        return {"error": "Username already exists"}

    # Validate uniqueness of email
    user_record = await get_user_record_util_user_info({'email': user_information.email})
    if user_record:
        return {"error": "Email already exists"}

    # If discord_id is provided, validate its uniqueness
    if user_information.discord_id:
        user_record = await get_user_record_util_user_info({'discord_id': user_information.discord_id})
        if user_record:
            return {"error": "Discord ID already exists"}
    

    if user_information.discord_id:
        return await create_user_record(user_information)
    
    else:
        return await create_user_record()

async def create_ruleset( user_information: Dict ) -> Dict:

    # Get user
    user_record = await get_user_record_util_user_info(user_information)
    if not user_record:
        return {"error": "User does not exist"}


    ruleset_record = await create_ruleset_record( user_record["_id"] )
    return ruleset_record


async def update_ruleset(ruleset_id: str, user_information: Dict, updates: Dict) -> Dict:

    # Get the ruleset
    ruleset_record = await get_ruleset_record(ruleset_id)
    if not ruleset_record:
        return {"error": "Ruleset does not exist"}
    if "error" in ruleset_record:
        return {"error": "User does not have permission to update record"}

    # Get the user record
    user_record = await get_user_record_util_user_info(user_information)
    if not user_record:
        return {"error": "User does not exist"}

    permissions_list = ruleset_record["permissions"]
    permissions_list.append(ruleset_record["owner_id"])

    # Validate whether the user has permissions
    permission = await validate_user_permissions(user_record, permissions_list)
    if not permission:
        return {"error": "User does not have required permissions"}

    # Call update_ruleset_record to make the updates
    update_result = await update_ruleset_record(ruleset_id, updates)

    if not update_result.get('updatedExisting'):
        return {"error": "Update failed"}
    
    # Check if the change is created by the owner and if not create a notification for the owner
    if user_record['_id'] != ruleset_record["owner_id"]:
        notification_creation_response = create_user_notification_record(ruleset_record['owner_id'], f"A ruleset you own has been changed by {user_record['_id']}")

        if "error" in notification_creation_response:
            print({"error": "Error in creating a notification for ruleset update"})
        
    return update_result

async def update_ruleset_record(ruleset_id: str, updates: Dict) -> Dict:
    # Use the $set operator to update the fields specified in the updates dictionary
    result = await db.rulesets.update_one({"_id": ObjectId(ruleset_id)}, {"$set": updates})
    return result.raw_result

def secure_string_formatting(string: str, dictionary: dict) -> str:
    """
    Function to safely replace placeholders in a string with dictionary values.

    Args:
        string (str): The string with placeholders.
        dictionary (dict): The dictionary with replacement values.

    Returns:
        str: The formatted string.
    """
    try:
        return string.format_map(dictionary)
    except KeyError as e:
        print(f"Missing key in dictionary: {e}")
        return string
    
async def create_project_record(base_project: Dict, user_id: str):

    new_project = base_project
    new_project['created_by'] = ObjectId(user_id)
    new_project['created_at'] = datetime.datetime.now()
    new_project['client'] = ObjectId(user_id)

    insert_result = await db.projects.insert_one(new_project)
    return insert_result


async def create_project(ruleset_id: str, user_id: Dict, init_fields: Dict, parents: list = None) -> Dict:
    #get user
    user_record = await get_user_record_util_user_info(user_id)

    if not user_record:
        return {"error": "User does not exist"}
            
    if ruleset_id != None:

        ruleset_record = await get_ruleset_record(ruleset_id)

        if not ruleset_record:
            return {"error": "Ruleset does not exist"}
        
        submission_fields = []
        
        if ruleset_record['ruleset_dependents'] != []:
            for dependent_ruleset_arr in ruleset_record['ruleset_dependents']:
                for dependent_ruleset_id in dependent_ruleset_arr:
                    dependent_ruleset = await get_ruleset_record(dependent_ruleset_id)
                    if not ruleset_record:
                        return {"error": "Ruleset does not exist"}
                    submission_fields.extend(dependent_ruleset['init_fields'])
                                 

        # Validate whether the user has permissions
        permission = await validate_user_permissions(ruleset_record, user_record, "create")
        
        if not permission:
            return {"error": "User does not have required permissions"}
        
        # Create project from base with 
        _base_project = ruleset_record['project_template']

        if _base_project['timeframe'] != { "days": 0, "hours": 0, "minutes": 0 }:
            _base_project['end_date'] = datetime.datetime.now() + datetime.timedelta(days=ruleset_record['timeframe']['days'], hours=ruleset_record['timeframe']['hours'], minutes=ruleset_record['timeframe']['minutes'])
        
        if parents:
            _base_project['parents'] = parents

        _base_project['init_values'] = init_fields
        _base_project['submission_fields'].extend(submission_fields)
        _base_project['ruleset_id'] = ruleset_record['_id']

        _base_project['description'] = secure_string_formatting(_base_project['description'], init_fields)
        
    if ruleset_id == None:
        _base_project = project_base()
        
    project_record = await create_project_record(_base_project, user_record['_id'])

    # Let users know that a project has been created for them to claim
    for permission in _base_project['permissions']:
        if permission['permission_type'] == "user" and permission['permission'] == "claim" and _base_project['status'] == "not_started":
            notification_creation_response = await create_user_notification_record(permission['permission_id'], "A project you can claim has been has been created")
            if "error" in notification_creation_response:
                print({"error": "Error in creating a notification for ruleset update"})

        elif permission['permission_type'] == "group" and permission['permission'] == "claim" and _base_project['status'] == "not_started":
            notification_creation_response = await create_group_user_notification_records(permission['permission_id'], "A project you can claim has been has been created")
            if "error" in notification_creation_response:
                print({"error": "Error in creating a notification for ruleset update"})

    if user_record['_id'] != ruleset_record["owner_id"]:
        notification_creation_response = create_user_notification_record(ruleset_record['owner_id'], f"A project has been instigated from a ruleset you own by: {user_record['_id']}")
        if "error" in notification_creation_response:
            print({"error": "Error in creating a notification for ruleset update"})

    return project_record

async def claim_project(project_id: str, user_id: Dict) -> Dict:

    # Get user record
    user_record = await get_user_record_util_user_info(user_id)
    if not user_record:
        return {"error": "User does not exist"}

    # Get project record
    project_record = await get_project_record(str(project_id))

    if not project_record:
        return {"error": "Project does not exist"}
    
    if project_record['status'] != "not_started":
        return {"error": "Project does not exist"}
    
    # Check permissions
    permission = await validate_user_permissions(project_record, user_record, "claim")
        
    if not permission:
        return {"error": "User does not have required permissions"}
    
    update_values = {
        "$set": {
            "worker": user_record['_id'],
            "status": "in_progress",
        }
    }

    if project_record['timeframe'] != { "days": 0, "hours": 0, "minutes": 0 }:
        update_values['$set']['start_date'] = datetime.datetime.now()
        update_values['$set']['due_date'] = datetime.datetime.now() + datetime.timedelta(days=project_record['timeframe']['days'], hours=project_record['timeframe']['hours'], minutes=project_record['timeframe']['minutes'])

    # Update project
    update_record_response = await update_project_record(project_record['_id'], update_values)

    return update_record_response

async def claimable_projects(user_id: Dict) -> Dict:

    user_record = await get_user_record_util_user_info(user_id)

    if not user_record:
        return {"error": "User does not exist"}

    permissions = await get_user_permissions(user_record)    
    project_record = await get_projects(permissions)

    return project_record

async def active_projects(user_id: Dict) -> Dict:
    
    user_record = await get_user_record_util_user_info(user_id)

    if not user_record:
        return {"error": "User does not exist"}
   
    project_record = await get_active_projects(str(user_record['_id']))

    return project_record

async def user_projects(user_id: Dict) -> Dict:
    # Get user record
    user_record = await get_user_record_util_user_info(user_id)
    if not user_record:
        return {"error": "User does not exist"}
        
    project_record = await get_user_projects(user_record['_id'])
    return project_record

async def claimable_reviews(user_id: Dict) -> Dict:

    user_record = await get_user_record_util_user_info(user_id)
    if not user_record:
        return {"error": "User does not exist"}

    permissions = await get_user_permissions(user_record)
    project_record = await get_review_projects(permissions)
    return project_record

async def active_reviews(user_id: Dict) -> Dict:
    # Get user record
    user_record = await get_user_record_util_user_info(user_id)
    if not user_record:
        return {"error": "User does not exist"}
        
    project_record = await get_active_reviews(user_record['_id'])

    return project_record

ALLOWED_RULESET_FIELDS = {"init_fields", "description", "data_set", "timeframe", "ruleset_dependents", "ruleset_dependencies"}
ALLOWED_TIMEFRAME_FIELDS = {"days", "hours", "minutes"}


async def validate_ruleset_updates(updates: dict) -> Dict:
    # Check that updates is a dictionary
    if not isinstance(updates, dict):
        return {"error": "Updates must be a dictionary"}

    # Check that all keys in updates are allowed
    for key in updates.keys():
        if key not in ALLOWED_RULESET_FIELDS: 
            return {"error": f"Invalid field in updates: {key}"}

    # Check the types of the updates
    for key, value in updates.items():
        if key == "timeframe" and not isinstance(value, dict):
            return {"error": "timeframe must be a dictionary"}

        if key == "timeframe":
            for sub_key in value.keys():
                if sub_key not in ALLOWED_TIMEFRAME_FIELDS:
                    return {"error": f"Invalid field in timeframe: {sub_key}"}

                if not isinstance(value[sub_key], (int, float)) or value[sub_key] < 0:
                    return {"error": f"{sub_key} in timeframe must be a positive number"}

    return {"Success": "Ruleset Update has been validated"}


ALLOWED_FIELDS = {"description", "due_date", "status", "payment"}
ALLOWED_STATUS = {"not_started", "in_progress", "completed", "reviewed"}

async def validate_updates(updates: dict) -> dict:
    # Check that updates is a dictionary
    if not isinstance(updates, dict):
        return {"error": "Updates must be a dictionary"}

    # Check that all keys in updates are allowed
    for key in updates.keys():
        if key not in ALLOWED_FIELDS:
            return {"error": f"Invalid field in updates: {key}"}

    # Check the types and values of the updates
    for key, value in updates.items():
        if key == "description" and not isinstance(value, str):
            return {"error": "description must be a string"}

        if key == "due_date":
            try:
                parse(value)
            except ValueError:
                return {"error": "due_date must be a string in the format YYYY-MM-DDTHH:MM:SS.SSSSSS"}

        if key == "status" and value not in ALLOWED_STATUS:
            return {"error": "status must be one of the following: not_started, in_progress, completed, reviewed"}

        if key == "payment" and (not isinstance(value, (int, float)) or value < 0):
            return {"error": "payment must be a positive number"}

    return {"Success": "Project Update has been validated"}

async def update_project_record(project_id: str, updates: Dict) -> Dict:
    result = await db.projects.update_one({"_id": ObjectId(project_id)}, updates)
    return result.raw_result


async def update_project(project_id: str, user_id: str, updates) -> Dict:

    # Validate the updates
    update_validated = await validate_updates(updates)

    if "error" in update_validated:
        return update_validated

    # Get the project ruleset
    project_record = await get_project_record(project_id)

    if not project_record:
        return {"error": "Project does not exist"}

    # Get the user record
    user_record = await get_user_record_util_user_info(user_id)


    if not user_record:
        return {"error": "User does not exist"}
    
    permissions_list = project_record['permissions']
    permissions_list.append(project_record['client'])

    # Validate whether the user has permissions
    permission = await validate_user_permissions(user_record, permissions_list)

    if not permission:
        return {"error": "User does not have required permissions"}

    # Call update_project_record to make the updates
    update_result = await update_project_record(project_id, updates)

    if not update_result.get('updatedExisting'):
        return {"error": "Update failed"}
        
    return update_result


async def update_project_progress(project_id: str, user_id: str, message: str, percentage: int) -> Dict:

    # Validate inputs
    try:
        assert (type(message) == str), "Message not a valid string"
        assert (percentage >= 0), "Percentage is not positive"
    except AssertionError as e:

        return {"error": "Caught an AssertionError: {e}"}

    # Get the project ruleset
    project_record = await get_project_record(project_id)

    if not project_record:
        return {"error": "Project does not exist"}

    # Get the user record
    user_record = await get_user_record_util_user_info(user_id)

    if not user_record:
        return {"error": "User does not exist"}
    

    if user_record['_id'] != project_record['worker']:
        return {"error": "User does not exist"}
    
    updates = {
        "project_percentage": percentage,
        "update_message": message,
        "update_datetime": datetime.datetime.now(),
        "user_id": user_record['_id']
    }
        

    # Call update_project_record to make the updates
    update_result = await update_project_record(project_id, {"$push": {"updates": updates}})

    if not update_result.get('updatedExisting'):
        return {"error": "Update failed"}
    
    # If behind alert the managers
    if project_record['due_date'] and project_record['start_date']:
        expected_percentage = (datetime.datetime.now() - project_record['start_date'])/(project_record['due_date'] - project_record['start_date'])

        if (percentage < expected_percentage-(expected_percentage*0.2)-10):

            manager_group_ids = [manager['_id'] for manager in project_record['permissions'] if manager['permission_type'] == "manager"]

            for manager_group_id in manager_group_ids:
                create_group_user_notification_records(manager_group_id, f"{project_record['worker_id']} is falling behind on project: {project_record['_id']} as he is currently {percentage} when expected percentage is {expected_percentage}")
        
    return {"success": f"Project was updated succesfully!"}


async def submit_project(project_id: str, user_info: Dict, submission: Dict) -> Dict:

    # Validate submission
 
    # Get the project ruleset
    project_record = await get_project_record(project_id)

    if not project_record:
        return {"error": "Project does not exist"}

    # Get the user record
    user_record = await get_user_record_util_user_info(user_info)

    if not user_record:
        return {"error": "User does not exist"}

    # Validate whether the user has permissions
    permission = await validate_user_permissions(project_record, user_record, "claim")

    if not permission:
        return {"error": "User does not have required permissions"}
    
    if project_record['status'] != "in_progress":
        return {"error": "Project cannot be submitted in its current state. Project status must be in_progress to be able to be submitted."}
    
    submission["submission_datetime"] = datetime.datetime.now()
    submission['user_id'] = user_record['_id']

    # Call update_project_record to make the updates
    updates = {"$push": {"submissions": submission}}
    project_id = project_record["_id"]

    if project_record["review_required"]:
        if len(project_record['reviews']) >= 1:
            if project_record['reviews'][-1]['status'] == 'rejected':
                updates["$set"] = {
                    "status": "in_review"
                }

                updates["$push"]['reviews'] = {
                    "worker_id" : project_record['reviews'][-1]["worker_id"],
                    "status": "in_progress",
                    "start_date": datetime.datetime.now(),
                    "due_date": datetime.datetime.now() + datetime.timedelta(days=project_record['review_timeframe']['days'], hours=project_record['review_timeframe']['hours'], minutes=project_record['review_timeframe']['minutes'])
                }

        else:  
            updates["$set"] = {"status": "awaiting_review"}
    else:
        updates["$set"] = {"status": "completed"}

    # Update the project in the database
    result = await db.projects.update_one({"_id": ObjectId(project_id)}, updates)

    if not result.matched_count > 0:
        return {"error": "Project does not exist"}
        
    # Make sure a review is not required and brother projects are completed
    if not project_record['review_required']:
        cascade_project(project_id, project_record['ruleset_id'])
    
    else:
        review_group_permissions = [permission['permission_id'] for permission in project_record['permissions'] if permission['permission'] == "review" and permission['permission_type'] == "group"]
        for review_permission_group in review_group_permissions:
            notification_creation_response =await create_group_user_notification_records(review_permission_group, "A project has been submitted in which you can review")
            if "error" in notification_creation_response:
                print({"error": "Error in creating a notification for ruleset update"})
        review_user_permissions = [permission['permission_id'] for permission in project_record['permissions'] if permission['permission'] == "review" and permission['permission_type'] == "user"]
        for review_permission_user in review_user_permissions:
            notification_creation_response = await create_user_notification_record(review_permission_user, "A project has been submitted in which you can review")
            if "error" in notification_creation_response:
                print({"error": "Error in creating a notification for ruleset update"})

    return {"success": f"Project submitted: {result}"}

async def cascade_project(project_id: str) -> Dict:
    # Fetch the project record from the database
    project_record = await get_project_record(project_id)
    if not project_record:
        return {"error": "Project does not exist"}
    
    # Fetch the ruleset record from the database
    ruleset_record = await get_ruleset_record(project_record['ruleset_id'])
    if not ruleset_record:
        return {"error": "Ruleset does not exist"}
    
    # Fetch brother projects
    brother_projects = []
    for brother_id in project_record['brothers']:
        brother_record = await get_project_record(brother_id)
        if brother_record:
            brother_projects.append(brother_record)
        else:
            return {"error": f"Brother project {brother_id} does not exist"}

    # Check that all brother projects are finished
    for brother_record in brother_projects:
        if brother_record['status'] != 'approved':
            return {"error": f"Brother project {brother_record['id']} is not completed"}

    # Gather the submission data from the project and the brother projects
    all_data = {**project_record['submissions'][-1]}
    for brother_record in brother_projects:
        all_data.update(brother_record['submissions'])

    all_submission_sets = create_submission_sets(all_data)

    print(all_submission_sets)

    all_created_projects = []
    for submission_data in all_submission_sets:
        # Create projects based on ruleset
        for subsequent_ruleset_set in ruleset_record['ruleset_dependents']:
            created_project_ids = []
            for subsequent_ruleset_id in subsequent_ruleset_set:
            # Merge project's submission data with brother data, prioritizing project's submission data
                init_fields = {**submission_data}
                new_project = await create_project(subsequent_ruleset_id, {"_id": project_record['created_by']}, init_fields, parents=project_id)
                created_project_ids.append(new_project.inserted_id)

            for created_project_id in created_project_ids:
                await update_project_record(created_project_id, {"$set": {"brothers": []}})
            
            all_created_projects.extend(created_project_ids)

        for brother_record in brother_projects:
            await update_project_record(brother_record['_id'], {"children": all_created_projects})
    
    return {"success": "New projects have been created", "Created_Project_IDs": all_created_projects}

def create_submission_sets(submission):
    
    max_length = max(
        (len(value) for value in submission.values() if isinstance(value, list)), 
        default=0
    )
    
    def create_new_dictionary_for_index(index):
        new_dict = {}
        for key, value in submission.items():
            if isinstance(value, list):
                if 0 <= index < len(value):
                    new_dict[key] = value[index]
                else:
                    new_dict[key] = None
            else:
                new_dict[key] = value
        return new_dict
    
    return [create_new_dictionary_for_index(i) for i in range(max_length)]


async def claim_review(project_id: str, user_id: Dict) -> Dict:
    # Get User record
    user_record = await get_user_record_util_user_info(user_id)
    if not user_record:
        return {"error": "User does not exist"}
    
    #get project record
    project_record = await get_project_record(str(project_id))
    if not project_record:
        return {"error": "Project does not exist"}

    #check permissions
    permission = await validate_user_permissions(project_record, user_record, "review")
    if not permission:
        return {"error": "User does not have required permissions"}
    
    #update project
    update_record_response = await update_project_record(project_record['_id'], {
        "$set": {
            "status": "in_review"
        },
        "$push": {
            "reviews": {
                "worker_id" : user_record['_id'],
                "status": "in_progress",
                "start_date": datetime.datetime.now(),
                "due_date": datetime.datetime.now() + datetime.timedelta(days=project_record['review_timeframe']['days'], hours=project_record['review_timeframe']['hours'], minutes=project_record['review_timeframe']['minutes'])
            }
        }
    })

    notification_creation_response = await create_user_notification_record(str(project_record['worker']), "Your project is now under review!")
    if "error" in notification_creation_response:
        print({"error": "Error in creating a notification for ruleset update"})
    return update_record_response


async def validate_review(review_details: Dict) -> Dict:
    return {"success": "success_messsage"}

async def review_project(project_id: str, user_id: str, review_details: Dict) -> Dict:

    # Validate the review_details
    review_validated = await validate_review(review_details)

    if "error" in review_validated:
        return review_validated

    # Get the project record
    project_record = await get_project_record(project_id)

    if not project_record:
        return {"error": "Project does not exist"}

    # Get the user record
    user_record = await get_user_record_util_user_info(user_id)

    if not user_record:
        return {"error": "User does not exist"}

    # Validate whether the user has permissions
    permission = await validate_user_permissions(project_record, user_record, "review")

    if not permission:
        return {"error": "User does not have required permissions"}

    # Check project status
    if project_record['status'] != 'in_review':
        return {"error": "Project status must be 'in_review' to be reviewed"}
    
    last_submission = project_record['reviews'][-1]
    last_submission['submission_datetime'] = datetime.datetime.now()
    last_submission['submission_message'] = review_details['submission_message']
    last_submission['status'] = review_details['status']

    # Call update_project_record to make the updates
    updates = {
        "$set": {
            'reviews': project_record['reviews']
        }
    }

    if review_details['status'] == "rejected":
        updates['$set']['status'] = "in_progress"
        await create_user_notification_record(str(project_record['worker']), "Your project has been reviewed but rejected!")
        
    else:
        updates['$set']['status'] = "approved"
        notification_creation_response = await create_user_notification_record(str(project_record['worker']), "Your project has been reviewed and approved! Congrats!")
        if "error" in notification_creation_response:
            print({"error": "Error in creating a notification for ruleset update"})

    update_result = await update_project_record(project_id, updates)

    if not update_result.get('updatedExisting'):
        return {"error": "Update failed"}
    
    if review_details['status'] == "approved":
        await cascade_project(project_id)
        
    return update_result

async def remove_user_from_project( project_record ):

    update_record = {
        "past_workers": project_record['past_workers'].append(project_record['worker']),
        "worker": None,
        "status": "not_started",
        "start_date": None,
        "due_date": None
    }

    await update_project_record(project_record['_id'], update_record)

    create_user_notification_record(project_record['worker'], "Your project was not updated for prolonged period of time. Project has been re-entered into the project pool.")


#async def removed_user_submission():

async def create_project_user_checkin_nofitications():

    user_active_projects = await get_all_user_active_projects_older_than_input(days_old=1)

    for project in user_active_projects:

        last_update = project['start_date']

        #may need to check who updated it
        if project['updates'] != []:
            if project['updates'][-1]['user_id'] == project['worker']:
                last_update = project['updates'][-1]['update_datetime']

        if project['submissions'] != []:
            if project['submissions'][-1]['user_id'] == project['worker']:
                if project['submissions'][-1]['submission_datetime'] > last_update:
                    last_update = project['submissions'][-1]['submission_datetime']

        if last_update < datetime.datetime.now() - datetime.timedelta(days=1):
            await create_user_notification_record(project['worker'], "Hey friendly daily reminder to update your project")

        elif last_update < datetime.datetime.now() - datetime.timedelta(days=2):
            await create_user_notification_record(project['worker'], "You haven't updated the project progress in more than a day. Please make sure to update your project regularly to avoid consequences.")
            
        elif last_update < datetime.datetime.now() - datetime.timedelta(days=3):
            await remove_user_from_project(project)