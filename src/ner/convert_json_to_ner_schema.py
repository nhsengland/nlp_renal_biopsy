def convert_to_bio(entity_data, texts):
    bio_tags = {}

    for text_id, entities in entity_data.items():
        text = texts[text_id]
        tags = ['O'] * len(text)

        for entity_list in entities.values():
            for entity in entity_list:
                start, end, label = entity['start'], entity['end'], entity['label']
                tags[start] = f'B-{label}'  # Beginning of entity
                for i in range(start + 1, end):
                    tags[i] = f'I-{label}'  # Inside of entity

        bio_tags[text_id] = list(zip(text, tags))

    return bio_tags

def convert_to_bioes(entity_data, texts):
    bioes_tags = {}

    for text_id, entities in entity_data.items():
        text = texts[text_id]
        tags = ['O'] * len(text)

        for entity_list in entities.values():
            for entity in entity_list:
                start, end, label = entity['start'], entity['end'], entity['label']
                if end - start == 1:  # Singleton entity
                    tags[start] = f'S-{label}'  # Singleton entity
                else:
                    tags[start] = f'B-{label}'  # Beginning of entity
                    for i in range(start + 1, end - 1):
                        tags[i] = f'I-{label}'  # Inside of entity
                    tags[end - 1] = f'E-{label}'  # End of entity

        bioes_tags[text_id] = list(zip(text, tags))

    return bioes_tags

# Example usage
bioes_output = convert_to_bioes(entity_data, texts)
for text_id, sentence in bioes_output.items():
    print(f"Text ID {text_id}: {sentence}")