import spacy


class EntityExtractor:

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

    def extract(
        self,
        text: str
    ):

        doc = self.nlp(text)
        
        entities = {
            "people": [],
            "organizations": [],
            "countries": [],
        }
        
        financial_orgs = [
            "SEBI",
            "RBI",
            "NSE",
            "BSE",
            "Jio",
            "Reliance",
            "TCS",
            "Infosys",
            "HDFC",
        ]

        for org in financial_orgs:

            if org.lower() in text.lower():

                entities["organizations"].append(
                    org
                )
                
        financial_people = [
            "Mukesh Ambani",
            "Nirmala Sitharaman",
            "Elon Musk",
            "Tim Cook",
            "Satya Nadella",
        ]

        for person in financial_people:

            if person.lower() in text.lower():

                entities["people"].append(
                    person
                )

        for ent in doc.ents:

            if ent.label_ == "PERSON":

                entities["people"].append(
                    ent.text
                )

            elif ent.label_ == "ORG":

                entities["organizations"].append(
                    ent.text
                )

            elif ent.label_ in [
                "GPE",
                "LOC"
            ]:

                entities["countries"].append(
                    ent.text
                )

        for key in entities:

            entities[key] = list(
                set(
                    entities[key]
                )
            )

        return entities