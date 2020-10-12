from src.preparation.data_access.obtained_text_da import ObtainedTextDA

if __name__ == "__main__":
    da = ObtainedTextDA()
    sentence_pairs = da.select_all_sentence_pairs_clean_as_list()
    with open('/home/hans/Proyectos/Python/Tesis_Chatbot/data/processed/csv_data.csv', 'w') as f:
        for sp in sentence_pairs:
            f.write(f'{",".join(sp)}\n')