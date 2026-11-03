"""EXCERPT of src/agents/voice_call_intelligence.py (production repo).
Real LangGraph graph: planner fans out to 4 concurrent nodes (router, extractor,
synthesizer, compliance). Extraction/summary nodes call an LLM; the compliance
node writes an audit receipt for the AI classification as its own concern."""
async def compliance_node(state: CallState) -> dict:
    """Persists the compliance receipt for the AI classification action.
    Its own node, its own concern -- not bolted onto the webhook handler
    after the fact. Doesn't touch CallState's output fields, only records
    the audit trail as a side effect."""
    try:
        await record_call_receipt(
            call_id=state["call_id"], tool="ai_intent_classification",
            arguments={"intent": state["intent"]}, outcome="classified",
            risk_classification="medium",
        )
    except Exception as e:
        logger.warning("[VoiceCallIntelligence] compliance_node failed: %s", e)
    return {}


async def _run_with_langgraph(initial_state: CallState) -> CallState | None:
    try:
        from langgraph.graph import StateGraph, END
    except ImportError:
        return None
    workflow = StateGraph(CallState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("router", router_node)
    workflow.add_node("extractor", extractor_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("compliance", compliance_node)
    workflow.set_entry_point("planner")
    # Four independent branches off planner -- LangGraph runs nodes with no
    # edge between each other concurrently, not sequentially.
    for branch in ("router", "extractor", "synthesizer", "compliance"):
        workflow.add_edge("planner", branch)
        workflow.add_edge(branch, END)
    graph = workflow.compile()
    return await graph.ainvoke(initial_state)


async def classify_call(transcript: str, call_id: str = "") -> dict:
