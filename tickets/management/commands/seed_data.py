from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from customers.models import Customer
from agents.models import Agent
from tickets.models import Ticket, TicketComment

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial realistic data for SupportAI backend'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # 1. Create Admin User
        admin_user, _ = User.objects.get_or_create(
            email="sarah.wilson@supportai.com",
            defaults={
                "username": "sarah.wilson@supportai.com",
                "name": "Sarah Wilson",
                "role": "Admin",
                "is_staff": True,
                "is_superuser": True
            }
        )
        admin_user.set_password("password123")
        admin_user.save()

        # 2. Create Support Agents
        agent_list = [
            ("Sarah Wilson", "sarah.wilson@supportai.com", "Senior Support Engineer", ["Django", "Python", "REST API", "Payment Support", "PostgreSQL"], 78, 4.9),
            ("Alex Rivera", "alex.rivera@supportai.com", "Technical Specialist", ["React", "JavaScript", "API Integration", "Authentication"], 90, 4.8),
            ("Emily Chen", "emily.chen@supportai.com", "Billing Lead", ["Payment Support", "Refunds", "Stripe", "Invoicing"], 45, 4.95),
            ("Michael Brown", "michael.brown@supportai.com", "Infrastructure Engineer", ["Docker", "PostgreSQL", "Django", "Cloud Hosting"], 65, 4.7),
            ("Jessica Taylor", "jessica.taylor@supportai.com", "Customer Success Agent", ["Onboarding", "Account Management", "General Support"], 30, 4.85),
            ("David Kim", "david.kim@supportai.com", "Full Stack Engineer", ["Django", "React", "Python", "GraphQL"], 82, 4.88),
            ("Rachel Adams", "rachel.adams@supportai.com", "Tier 1 Specialist", ["Account", "Password Reset", "General Support"], 50, 4.92),
            ("Marcus Vance", "marcus.vance@supportai.com", "API Engineer", ["REST API", "Webhooks", "OAuth2", "Python"], 60, 4.75),
        ]

        created_agents = []
        for name, email, role, skills, workload, rating in agent_list:
            u, _ = User.objects.get_or_create(
                email=email,
                defaults={"username": email, "name": name, "role": "Agent"}
            )
            u.set_password("password123")
            u.save()

            ag, _ = Agent.objects.get_or_create(
                user=u,
                defaults={
                    "role": role,
                    "skills": skills,
                    "workload": workload,
                    "customer_rating": rating,
                    "total_assigned": 12,
                    "total_resolved": 340
                }
            )
            created_agents.append(ag)

        # 3. Create Customers
        customer_list = [
            ("John Smith", "john.smith@acme.corp", "+1 (555) 234-5678", "Acme Corporation", "Enterprise"),
            ("Elena Rostova", "elena@techwave.io", "+1 (555) 876-5432", "TechWave Inc", "Pro"),
            ("David Miller", "d.miller@fintechlabs.com", "+1 (555) 345-6789", "FinTech Labs", "Enterprise"),
            ("Sophia Martinez", "sophia@cloudscale.net", "+1 (555) 456-7890", "CloudScale Networks", "Pro"),
            ("Amanda Clark", "aclark@globalpay.com", "+1 (555) 678-9012", "Global Pay", "Enterprise"),
        ]

        created_customers = []
        for name, email, phone, company, tier in customer_list:
            c, _ = Customer.objects.get_or_create(
                email=email,
                defaults={"name": name, "phone": phone, "company": company, "tier": tier}
            )
            created_customers.append(c)

        # 4. Create Sample Tickets
        sample_tickets = [
            ("TK-1024", created_customers[0], "Payment failed during checkout with code ERR_PAY_5002", "I attempted to upgrade our Enterprise subscription, but payment gateway timed out.", "PAYMENT", "HIGH", "OPEN", "NEGATIVE", created_agents[0]),
            ("TK-1025", created_customers[1], "REST API Endpoint returning 500 internal server error on webhook dispatch", "When subscribing to 'ticket.updated' event, payload fails with 500 error code.", "TECHNICAL", "CRITICAL", "IN_PROGRESS", "NEUTRAL", created_agents[1]),
            ("TK-1026", created_customers[2], "Unable to reset password via SSO link", "Our OKTA SSO integration is rejecting password reset tokens sent from login portal.", "ACCOUNT", "MEDIUM", "WAITING", "NEGATIVE", created_agents[6]),
            ("TK-1027", created_customers[4], "Request for invoice refund on annual billing tier", "We downgraded seat allocation last week, but were charged full original seat count.", "REFUND", "HIGH", "OPEN", "NEGATIVE", created_agents[2]),
            ("TK-1028", created_customers[3], "Hardware license key delivery confirmation", "Received hardware order confirmation but haven't received digital license keys via email.", "DELIVERY", "LOW", "RESOLVED", "POSITIVE", created_agents[4]),
        ]

        for num, customer, subject, desc, cat, prio, stat, sent, agent in sample_tickets:
            t, _ = Ticket.objects.get_or_create(
                ticket_number=num,
                defaults={
                    "customer": customer,
                    "subject": subject,
                    "description": desc,
                    "category": cat,
                    "priority": prio,
                    "status": stat,
                    "sentiment": sent,
                    "assigned_agent": agent,
                    "ai_confidence": 0.94,
                    "required_skills": ["Payment Support", "REST API"],
                    "ai_suggested_response": f"Hello {customer.name},\n\nWe have received your ticket regarding '{subject}'. Our engineering team is currently investigating."
                }
            )

            # Add initial comment
            TicketComment.objects.get_or_create(
                ticket=t,
                user=admin_user,
                defaults={"message": desc}
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded database with users, agents, customers, and tickets!"))
