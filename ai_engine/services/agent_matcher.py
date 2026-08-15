from agents.models import Agent

def match_and_assign_agent(required_skills: list) -> Agent:
    """
    Finds matching available agents, checks workload, calculates match score (0-100),
    recommends and returns the best agent object.
    """
    active_agents = Agent.objects.filter(status='ONLINE').order_by('workload')
    if not active_agents.exists():
        active_agents = Agent.objects.all().order_by('workload')

    if not active_agents.exists():
        return None

    best_agent = None
    best_score = -1

    for agent in active_agents:
        # Calculate skill overlap score
        agent_skills = [s.lower() for s in (agent.skills or [])]
        req_skills = [s.lower() for s in required_skills]
        
        matches = sum(1 for req in req_skills if any(req in skill or skill in req for skill in agent_skills))
        skill_score = (matches / max(len(req_skills), 1)) * 60  # Max 60 points for skills
        
        workload_score = (100 - agent.workload) * 0.4  # Max 40 points for low workload
        total_score = round(skill_score + workload_score)

        if total_score > best_score:
            best_score = total_score
            best_agent = agent

    if best_agent:
        best_agent.total_assigned += 1
        best_agent.workload = min(100, best_agent.workload + 5)
        best_agent.save()

    return best_agent or active_agents.first()
