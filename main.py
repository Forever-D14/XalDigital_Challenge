import datetime as dt
import requests
import pandas as pd


class Verifier:

    def __init__(self, url: str):
        self.api_url: str = url

    def main(self) -> None:

        answers = self.get_response_n_transform_to_df(self.api_url)
        self.answered_n_unanswered(answers)
        self.minor_view(answers)
        self.oldest_n_last(answers)
        self.highest_reputation(answers)

    def get_response_n_transform_to_df(self, api_url: str) -> pd.DataFrame:

        response = requests.get(api_url)

        answers_json = response.json()['items']
        answers = pd.DataFrame(answers_json)

        owners_info = pd.DataFrame(list(answers['owner']))

        final_answers_df = answers.join(owners_info, rsuffix='_owner').drop("owner", axis=1)
        final_answers_df['creation_date'] = final_answers_df['creation_date'].map(lambda x: dt.datetime.fromtimestamp(x))

        return final_answers_df

    def answered_n_unanswered(self, answers_df: pd.DataFrame) -> None:
        answered_answers = answers_df[answers_df['is_answered']]['is_answered'].count()
        unanswered_answers = answers_df['is_answered'].count() - answered_answers

        print(f'''
            RESPUESTAS CONTESTADAS Y NO CONTESTADAS
            - CONTESTADAS: {answered_answers} respuestas
            - NO CONTESTADAS: {unanswered_answers} respuestas
            ''')

    def minor_view(self, answers_df: pd.DataFrame) -> None:
        '''
        Obtiene la o las respuestas con menos numero de
        vistas. Imprime cada una de ellas con su titulo
        y la cantidad de visitas
        '''
        minor_view = answers_df['view_count'].min()
        minor_view_answers = answers_df[answers_df['view_count'] == minor_view]['title']

        print('''
            RESPUESTA(s) CON MENOS VISTAS''')
        for i, answer in enumerate(minor_view_answers):
            print(f'\t{i}.- TITULO: {answer}\n'
                  f'\t  - VISTAS: {minor_view} vistas')

    def oldest_n_last(self, answers_df: pd.DataFrame) -> None:
        '''
        Obtiene la respuesta mas vieja y mas actual del
        dataset. Imprime el titulo de cada respuesta
        '''
        oldest = answers_df['creation_date'].min()
        last = answers_df['creation_date'].max()

        oldest_answer = answers_df[answers_df['creation_date'] == oldest]['title'].iloc[0]
        last_answer = answers_df[answers_df['creation_date'] == last]['title'].iloc[0]

        print(f'''
            RESPUESTA MAS VIEJA Y MAS ACTUAL (Titulos)
            - VIEJA: {oldest_answer} 
            - ACTUAL: {last_answer}
        ''')

    def highest_reputation(self, answers_df: pd.DataFrame) -> None:
        '''
        Obtiene la respuesta del owner con mayor reputacion
        Puede llegar al caso en donde haya varias preguntas
        del mismo owner o varios owners con la misma
        reputacion. Se imprime cada uno de los owners con
        sus respectivas respuestas.
        '''
        high_reputation = answers_df['reputation'].max()
        highest_reputation_owners = answers_df[answers_df['reputation'] == high_reputation]['display_name']

        print('''
            RESPUESTA(s) DEL OWNER CON MAYOR REPUTACION''')
        for i, owner in enumerate(highest_reputation_owners):
            print(f'''\tOWNER {i}
                REPUTACION: {high_reputation}
                RESPUESTAS:''')
            owners_answers = answers_df[answers_df['display_name'] == owner]['title']
            for j, answer in enumerate(owners_answers):
                print(f'''\t\t{j}.- {answer}''')


verifier_test = Verifier("https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle=perl&site=stackoverflow")
verifier_test.main()
