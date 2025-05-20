# Example: Customer Support Flow with structured processing
from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel

from ..utils import print_message
from ..llm.client import model_client


def run() -> None:
    # Define structured state
    class SupportTicketState(BaseModel):
        ticket_id: str = ""
        customer_name: str = ""
        issue_description: str = ""
        category: str = ""
        priority: str = "medium"
        resolution: str = ""
        satisfaction_score: int = 0

    class CustomerSupportFlow(Flow[SupportTicketState]):
        @start()
        def receive_ticket(self):
            # In a real app, this might come from an API
            self.state.ticket_id = "TKT-12345"
            self.state.customer_name = "Alex Johnson"
            self.state.issue_description = (
                "Unable to access premium features after payment"
            )
            return "Ticket received"

        @listen(receive_ticket)
        def categorize_ticket(self, _):
            prompt = f"""
            Categorize the following customer support issue into one of these categories:
            - Billing
            - Account Access
            - Technical Issue
            - Feature Request
            - Other

            Issue: {self.state.issue_description}

            Return only the category name.
            """

            self.state.category = model_client.call(prompt).strip()
            return self.state.category

        @router(categorize_ticket)
        def route_by_category(self, category):
            # Route to different handlers based on category
            return category.lower().replace(" ", "_")

        @listen("billing")
        def handle_billing_issue(self):
            # Handle billing-specific logic
            self.state.priority = "high"
            # More billing-specific processing...
            return "Billing issue handled"

        @listen("account_access")
        def handle_access_issue(self):
            # Handle access-specific logic
            self.state.priority = "high"
            # More access-specific processing...
            return "Access issue handled"

        # Additional category handlers...

        @listen(
            or_(
                "billing",
                "account_access",
                "technical_issue",
                "feature_request",
                "other",
            )
        )
        def resolve_ticket(self, resolution_info):
            # Final resolution step
            self.state.resolution = f"Issue resolved: {resolution_info}"
            return self.state.resolution

    # Run the flow
    support_flow = CustomerSupportFlow()
    result = support_flow.kickoff()
    print_message(result)
