class WebHarvestWeaver:
    @staticmethod
    def compile_consensus_blocks(user_prompt: str, use_rag: bool, is_live_query: bool, has_local_context: bool, search_client) -> str:
        """Queries unbiased web indexes, triggers consensus grouping, and compiles reference text blocks."""
        if not use_rag or (not is_live_query and has_local_context):
            return ""

        print("[Orchestration Core]: Executing live multi-perspective web consensus analysis...")
        search_report = search_client.consensus_search(user_prompt, sample_size=6)
        groups = search_report.get("consensus_groups", [])
        
        if not groups:
            return ""

        web_context_blocks = []
        for idx, group in enumerate(groups, 1):
            source_links = ", ".join([s["url"] for s in group["sources"]])
            web_context_blocks.append(
                f"Claim Group {idx} (Agreement Weight: {group['consensus_weight']}):\n"
                f"Evidence Summary: {group['lead_text']}\n"
                f"Sources: [{source_links}]"
            )
        return "\n\n".join(web_context_blocks)
