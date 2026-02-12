from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

class TaskRepository:

    def __init__(self, table):
        self.table = table

    def create(self, task):
        self.table.put_item(Item=task.to_dict())

    def get_by_id(self, task_id):
        response = self.table.get_item(
            Key={
                "pk": "TASK",
                "sk": f"TASK#{task_id}"
            }
        )
        return response.get("Item")

    def get_all(self):
        items = []
        response = self.table.scan(
        FilterExpression=Attr("pk").eq("TASK")
    )
        items.extend(response.get("Items", []))

        # Paginação
        while "LastEvaluatedKey" in response:
            response = self.table.scan(
                FilterExpression=Attr("pk").eq("TASK"),
                ExclusiveStartKey=response["LastEvaluatedKey"]
            )
            items.extend(response.get("Items", []))

        return items

    def update(self, task_id, titulo, descricao, status, data_conclusao, criado_por):
        self.table.update_item(
            Key={
                "pk": "TASK",
                "sk": f"TASK#{task_id}"
            },
            UpdateExpression="""
                SET titulo = :t,
                    descricao = :d,
                    #s = :s,
                    data_conclusao = :dc
            """,
            ExpressionAttributeNames={
                "#s": "status"
            },
            ConditionExpression="criado_por = :cp",
            ExpressionAttributeValues={
                ":t": titulo,
                ":d": descricao,
                ":s": status,
                ":dc": data_conclusao,
                ":cp": criado_por
            },
        )
    def delete(self, task_id):
        self.table.delete_item(
            Key={
                "pk": "TASK",
                "sk": f"TASK#{task_id}"
            }
        )
