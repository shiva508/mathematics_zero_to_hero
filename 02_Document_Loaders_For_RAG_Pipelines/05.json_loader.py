from langchain_community.document_loaders import JSONLoader


def get_json_loader():
    json_file_path = "/home/shiva/PycharmProjects/mathematics_zero_to_hero/02_Document_Loaders_For_RAG_Pipelines/sample_json.json"
    json_loader = JSONLoader(file_path=json_file_path,
                             jq_schema=".",  # "." means load the whole list of objects
                             text_content=False  # We'll get structured documents instead of raw strings
                             )
    json_objects = json_loader.load()
    for json_object in range(len(json_objects)):
        print(json_objects[json_object])


if __name__ == "__main__":
    get_json_loader()
