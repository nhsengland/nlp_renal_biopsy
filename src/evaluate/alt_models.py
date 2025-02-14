from src.evaluate.report import evaluate_report
from tqdm import tqdm


def evaluate(annotated_json, predicted_json, eg, n_prototypes=20):
    e2i_map = eg.entity_to_info_map
    n_entities = len(e2i_map)
    all_scores = []

    for i, (anno, pred) in enumerate(
        tqdm(
            zip(annotated_json, predicted_json),
            total=n_prototypes,
            desc="Evaluating predictions",
            ncols=110,
        )
    ):
        if i == n_prototypes:
            break
        report_scores = evaluate_report(e2i_map, anno, pred)
        all_scores.append(report_scores)

    # Calculate scores
    scores_per_report = [
        round(sum(scores.values()) / n_entities, 3) for scores in all_scores
    ]

    final_score = round(sum(scores_per_report) / n_prototypes, 3)

    return all_scores, scores_per_report, final_score


def calculate_entity_accuracy(all_scores, eg):
    # Initialise results dictionary
    results = {
        entity: {
            "correct": 0,
            "total": len(all_scores),
        }
        for entity in eg.entity_to_info_map.keys()
    }

    # Process all scores
    for report_scores in all_scores:
        for entity, score in report_scores.items():
            results[entity]["correct"] += score

    # Calculate percentages
    for entity in results:
        total = results[entity]["total"]
        correct = results[entity]["correct"]
        results[entity]["accuracy"] = round((correct / total) * 100, 1)

    # Print results
    print("\nAccuracy per entity:")
    print("=" * 60)
    print(f"{'Entity':30} {'Score':15} {'Type':15}")
    print("-" * 60)

    for entity, scores in results.items():
        entity_type = eg.entity_to_info_map[entity][1]
        score_str = f"{scores['correct']}/{scores['total']} ({scores['accuracy']}%)"
        print(f"{entity:30} {score_str:15} {entity_type:15}")

    return results
