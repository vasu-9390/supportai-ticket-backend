from tickets.models import Ticket

def check_duplicate_ticket(subject: str, description: str) -> dict:
    open_tickets = Ticket.objects.exclude(status='CLOSED').order_by('-created_at')[:20]
    
    subj_words = set((subject or "").lower().split())
    desc_words = set((description or "").lower().split())
    input_tokens = subj_words.union(desc_words)

    best_match_id = None
    best_similarity = 0.0

    for t in open_tickets:
        t_tokens = set(t.subject.lower().split()).union(set(t.description.lower().split()))
        if not input_tokens or not t_tokens:
            continue
            
        intersection = input_tokens.intersection(t_tokens)
        similarity = len(intersection) / float(len(input_tokens.union(t_tokens)))
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_id = t.id

    is_duplicate = best_similarity >= 0.45
    return {
        "is_duplicate": is_duplicate,
        "similarity": round(best_similarity, 2),
        "related_ticket_id": best_match_id
    }
