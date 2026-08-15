from .gemini_service import generate_gemini_json

def generate_suggested_response_for_ticket(ticket) -> str:
    comments_summary = ""
    if ticket.comments.exists():
        comments_summary = "\n".join([f"- {c.user.name}: {c.message}" for c in ticket.comments.all()[:5]])

    prompt = f"""
    Generate a concise, professional, empathetic customer support resolution response for ticket:
    Subject: {ticket.subject}
    Description: {ticket.description}
    Category: {ticket.category}
    Priority: {ticket.priority}
    Previous Comments:
    {comments_summary}

    Return JSON: {{"suggested_response": "..."}}
    """

    gemini_res = generate_gemini_json(prompt, "You are a customer service AI response generator.")
    if gemini_res and isinstance(gemini_res, dict) and 'suggested_response' in gemini_res:
        return gemini_res['suggested_response']

    # Fallback
    return (
        f"Hello {ticket.customer.name},\n\n"
        f"Thank you for bringing this issue regarding '{ticket.subject}' to our attention. "
        f"Our team has analyzed the request ({ticket.get_category_display()} - {ticket.priority} Priority). "
        f"We have dispatched this ticket to our senior support engineers and will resolve it promptly.\n\n"
        f"Thank you for your patience!\n\nBest regards,\nSupportAI Team"
    )
