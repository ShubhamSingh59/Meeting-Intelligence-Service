import httpx
from core.config import config
from database.session import session_local
from models.action_item import ActionItem
from datetime import datetime


class WebhookService:
    def __init__(self):
        self.webhook_url = config.WEBHOOK_URL

    async def send_webhook(self):
        if self.webhook_url:
            print("No webhook URL configured. Skipping webhook call.")
            return

        db = session_local()
        try:
            current_time = datetime.utcnow()

            overdue_items = (
                db.query(ActionItem)
                .filter(
                    ActionItem.due_date < current_time, ActionItem.status != "COMPLETED"
                )
                .all()
            )

            if not overdue_items:
                print(
                    f"[{datetime.utcnow()}] No overdue items found. Background check complete."
                )
                return

            ## Sending the message to the webhook
            async with httpx.AsyncClient() as client:
                for item in overdue_items:
                    message = {
                        "content": f"OVERDUE TASK ALERT\n"
                        f"**Task:** {item.task}\n"
                        f"**Assignee:** {item.assignee}\n"
                        f"**Was Due:** {item.due_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"Please update the status immediately!"
                    }

                    response = await client.post(self.webhook_url, json=message)
                    print(
                        f"Reminder sent for Task ID {item.id} - Status Code: {response.status_code}"
                    )

        except Exception as e:
            print(f"Failed to run background webhook service: {str(e)}")
        finally:
            db.close()

notification_service = WebhookService()