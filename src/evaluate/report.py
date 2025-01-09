from .laaj import use_llm_to_compare

def evaluate_report(entity_to_info_map, json_1, json_2):
    report_scores_dict = {entity: 0 for entity in entity_to_info_map.keys()}

    for entity, metadata in entity_to_info_map.items():
        anno_value = json_1.get(entity, None)
        pred_value = json_2.get(entity, None)

        if metadata[1] in ['boolean', 'categorical', 'numerical']:
            if anno_value == pred_value:
                report_scores_dict[entity] += 1
        
        # else entity type is some sort of text string
        else:
            if use_llm_to_compare(anno_value, pred_value, llama_cpp=False):
                report_scores_dict[entity] += 1
    
    return report_scores_dict