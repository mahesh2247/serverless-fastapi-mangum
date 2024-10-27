# controllers/item_controller.py

from sqlalchemy.orm import Session
from models.item_model import Item
import boto3
import os
from botocore.exceptions import ClientError
from decimal import Decimal  # Import Decimal

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])  # Replace with your DynamoDB table name

def get_item_service(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def convert_to_decimal(item_data: dict) -> dict:
    """Convert float values in item_data to Decimal."""
    if 'price' in item_data:
        item_data['price'] = Decimal(str(item_data['price']))  # Convert float to Decimal
    return item_data

def create_item_service(db: Session, item_data: dict):
    db_item = Item(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Insert into DynamoDB
    item_data_for_dynamodb = convert_to_decimal(db_item.to_dict())  # Convert before inserting
    try:
        table.put_item(Item=item_data_for_dynamodb)
    except ClientError as e:
        raise Exception(f"Could not insert into DynamoDB: {str(e)}")

    return db_item

def update_item_service(db: Session, item_id: int, item_data: dict):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise Exception("Item not found")

    for key, value in item_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    # Update in DynamoDB
    item_data_for_dynamodb = convert_to_decimal(item.to_dict())  # Convert before updating
    try:
        table.update_item(
            Key={'id': item.id},
            UpdateExpression="set #n = :name, description = :desc, price = :price",
            ExpressionAttributeNames={
                '#n': 'name'
            },
            ExpressionAttributeValues={
                ':name': item_data_for_dynamodb['name'],
                ':desc': item_data_for_dynamodb['description'],
                ':price': item_data_for_dynamodb['price']
            }
        )
    except ClientError as e:
        raise Exception(f"Could not update DynamoDB: {str(e)}")

    return item

def delete_item_service(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise Exception("Item not found")

    db.delete(item)
    db.commit()

    # Delete from DynamoDB
    try:
        table.delete_item(
            Key={'id': item.id}  # Adjust as needed to match your table key
        )
    except ClientError as e:
        raise Exception(f"Could not delete from DynamoDB: {str(e)}")

