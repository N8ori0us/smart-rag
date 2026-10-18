class ConsensusProcessor:
    @staticmethod    
    def cluster_and_rate_perspectives(raw_results: list, original_prompt: str) -> dict:
        print("[Consensus Core Activated]: Clustering matching claims and cross-rating perspectives...")

        groups = []
        prompt_words = set(original_prompt.lower().split())

        for item in raw_results:
            content = item.get("content", "").strip()
            url = item.get("url", "")
            title = item.get("title", "")

            if not content or len(content) < 30:
                continue

            content_words = set(content.lower().split())
            prompt_relevance = len(content_words.intersection(prompt_words)) / max(len(prompt_words), 1)

            matched_existing_group = False
            for group in groups:
                lead_words = set(group["lead_text"].lower().split())
                overlap = len(content_words.intersection(lead_words)) /max(len(lead_words), 1)

                if overlap > 0.25:
                    group["sources"].append({"title": title, "url": url, "snippet": content})
                    group["consensus_weight"] += 1
                    if prompt_relevance > group["max_prompt_relevance"]:
                        group["max_prompt_relevance"] = prompt_relevance
                    matched_existing_group = True
                    break

            if not matched_existing_group:
                groups.append({
                    "lead_text": content,
                    "max_prompt_relevance": prompt_relevance,
                    "consensus_weight": 1,
                    "sources": [{"title": title, "url": url, "snippet": content}]
                })

        for group in groups:
            group["final_priority_score"] = group["consensus_weight"] * (1.0 + group["max_prompt_relevance"])

        groups.sort(key=lambda x: x ["final_priority_score"], reverse=True)

        print(f"Formed {len(groups)} distinct perspective clusters from {len(raw_results)} sources:")
        for idx, g in enumerate(groups, 1):
            print(f"Cluster {idx}: Weight (Agreement): {g['consensus_weight']} | Relevance: {g['max_prompt_relevance']:.2f} {len(g['sources'])}")

        return {
            "consensus_groups": groups,
            "raw_results_count": len(raw_results)
        }