import csv

from src.preparation.data_access.obtained_text_da import ObtainedTextDA

if __name__ == "__main__":
    '''da = ObtainedTextDA()
    # Grade 1
    sentence_pairs = da.select_all_sentence_pairs_by_grade_clean_as_list(1)
    with open('/home/hans/Proyectos/Python/Tesis_Chatbot/data/processed/csv_data_1.csv', 'w') as f:
        for sp in sentence_pairs:
            f.write(f'{",".join(sp)}\n')
    # Grade 2
    sentence_pairs =    da.select_all_sentence_pairs_by_grade_clean_as_list(2)
    with open('/home/hans/Proyectos/Python/Tesis_Chatbot/data/processed/csv_data_2.csv', 'w') as f:
        for sp in sentence_pairs:
            f.write(f'{",".join(sp)}\n')'''

    da = ObtainedTextDA()
    grades = [1, 2]
    categories = ['Historia, Geografía y Economía', 'CTA', 'Comunicación']
    
    for g in grades:
        for c in categories:
            with open(f'csv_data_{g}_{c}.csv', 'w') as csv_file:
                print(f'Writing file: csv_data_{g}_{c}.csv')
                csv_writer = csv.writer(csv_file)
                for sp in da.select_all_sentence_pairs_by_grade_and_category(g, c):
                    csv_writer.writerow(sp)