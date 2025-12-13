import os
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from complaints.models import Complaint

# Define State
class AgentState(TypedDict):
    complaint_id: int
    status: str
    urgency: int
    escalation_level: int
    draft_email: str
    recipient: str
    final_status: str

# Initialize LLM
# Initialize LLM
# llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ.get("GEMINI_API_KEY"))

# Node 1: Check Status
def check_status(state: AgentState):
    try:
        complaint = Complaint.objects.get(id=state["complaint_id"])
        print(f"🕵️‍♂️ Agent Checking Complaint #{complaint.id}...")
        
        # Logic: If Resolved, Stop. If High Urgency & Old, Escalate.
        if complaint.status == Complaint.Status.RESOLVED:
            return {"final_status": "RESOLVED"}
            
        # Check Time Threshold (e.g., 24 hours)
        time_diff = timezone.now() - complaint.created_at
        if time_diff > timedelta(hours=24) and complaint.urgency_score >= 8:
            return {"status": "NEEDS_ESCALATION", "urgency": complaint.urgency_score, "escalation_level": complaint.escalation_level}
        
        return {"final_status": "NO_ACTION_NEEDED"}
    except Complaint.DoesNotExist:
        return {"final_status": "ERROR"}

# Node 2: Draft Legal Notice (The "Legal Eagle" part)
def draft_notice(state: AgentState):
    print("⚖️ Drafting Legal Notice...")
    
    # Lazy Load LLM to prevent import-time errors during tests
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ.get("GEMINI_API_KEY"))
    
    complaint = Complaint.objects.get(id=state["complaint_id"])
    
    prompt = f"""
    You are a strict legal assistant for a civic grievance platform.
    Draft a formal escalation email for the following complaint:
    
    Category: {complaint.category}
    Description: {complaint.description}
    Location: {complaint.location_address}
    Ward: {complaint.ward.name if complaint.ward else 'Unknown'}
    Urgency: {complaint.urgency_score}/10
    Days Pending: {(timezone.now() - complaint.created_at).days}
    
    Cite 'Section 61 of the BMC Act' regarding duty to maintain public safety.
    Tone: Professional, Urgent, Authoritative.
    Subject Line: [LEGAL NOTICE] Immediate Action Required - Ref #{complaint.id}
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"draft_email": response.content}

# Node 3: Send Email
def send_email(state: AgentState):
    print("📧 Sending Escalation Email...")
    complaint = Complaint.objects.get(id=state["complaint_id"])
    
    # Determine Recipient
    recipient = settings.SENIOR_OFFICIALS.get('AMC_CITY', 'poojary.rupesh12@gmail.com')
    if settings.EMAIL_OVERRIDE_ADDRESS:
        recipient = settings.EMAIL_OVERRIDE_ADDRESS
        
    try:
        send_mail(
            subject=f"Escalation: Complaint #{complaint.id}", # Simplified subject for header
            message=state["draft_email"],
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient],
            fail_silently=False
        )
        return {"recipient": recipient}
    except Exception as e:
        print(f"❌ Email Failed: {e}")
        return {"final_status": "EMAIL_FAILED"}

# Node 4: Update Database
def update_db(state: AgentState):
    print("💾 Updating Database...")
    complaint = Complaint.objects.get(id=state["complaint_id"])
    complaint.escalation_level += 1
    complaint.status = Complaint.Status.ESCALATED
    complaint.save()
    return {"final_status": "ESCALATED"}

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("check_status", check_status)
workflow.add_node("draft_notice", draft_notice)
workflow.add_node("send_email", send_email)
workflow.add_node("update_db", update_db)

# Define Edges
def router(state: AgentState):
    if state.get("final_status"):
        return END
    if state.get("status") == "NEEDS_ESCALATION":
        return "draft_notice"
    return END

workflow.set_entry_point("check_status")
workflow.add_conditional_edges("check_status", router)
workflow.add_edge("draft_notice", "send_email")
workflow.add_edge("send_email", "update_db")
workflow.add_edge("update_db", END)

app = workflow.compile()

def run_escalation_agent(complaint_id):
    result = app.invoke({"complaint_id": complaint_id})
    return result
