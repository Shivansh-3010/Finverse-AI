from typing import Set


class AliasGenerator:

    COMPANY_SUFFIXES = {
        "limited",
        "ltd",
        "limited.",
        "ltd.",
    }
    
    GENERIC_FIRST_WORDS = {
        "state",
        "indian",
        "national",
        "global",
        "united",
        "power",
        "general",
        "tata",
        "adani",
        "bajaj",
        "mahindra",
        "apollo",
    }

    MANUAL_ALIASES = {
        "State Bank of India": ["SBI"],
        "Reliance Industries Limited": ["RIL"],
        "Tata Consultancy Services Limited": ["TCS"],
        "HDFC Bank Limited": ["HDFC"],
        "ICICI Bank Limited": ["ICICI"],
        "Life Insurance Corporation of India": ["LIC"],

        "Oil and Natural Gas Corporation Limited": ["ONGC"],
        "National Thermal Power Corporation Limited": ["NTPC"],
        "Indian Oil Corporation Limited": ["IOC"],
        "Bharat Petroleum Corporation Limited": ["BPCL"],
        "Hindustan Petroleum Corporation Limited": ["HPCL"],
        "Power Grid Corporation of India Limited": ["POWERGRID"],
        "Coal India Limited": ["CIL"],

        "Larsen & Toubro Limited": ["L&T", "LT"],
        "Mahindra & Mahindra Limited": ["M&M", "MM"],
        "Bajaj Auto Limited": ["BAJAJ"],
        "Bajaj Finance Limited": ["BAJFIN"],
        "Bajaj Finserv Limited": ["BAJAJFINSERV"],

        "Axis Bank Limited": ["AXIS"],
        "Kotak Mahindra Bank Limited": ["KOTAK"],
        "IndusInd Bank Limited": ["INDUSIND"],
        "Punjab National Bank": ["PNB"],
        "Bank of Baroda": ["BOB"],

        "Infosys Limited": ["INFY"],
        "Wipro Limited": ["WIPRO"],
        "HCL Technologies Limited": ["HCLTECH"],
        "Tech Mahindra Limited": ["TECHM"],
        "LTIMindtree Limited": ["LTIM"],
        "Mphasis Limited": ["MPHASIS"],

        "Tata Motors Limited": ["TATAMOTORS"],
        "Maruti Suzuki India Limited": ["MARUTI"],
        "Eicher Motors Limited": ["EICHER"],
        "Hero MotoCorp Limited": ["HERO"],
        "TVS Motor Company Limited": ["TVS"],

        "Adani Enterprises Limited": ["ADANI"],
        "Adani Ports and Special Economic Zone Limited": ["ADANIPORTS"],
        "Adani Green Energy Limited": ["ADANIGREEN"],
        "Adani Power Limited": ["ADANIPOWER"],
        "Adani Total Gas Limited": ["ATGL"],

        "Sun Pharmaceutical Industries Limited": ["SUNPHARMA"],
        "Dr. Reddy's Laboratories Limited": ["DRREDDY"],
        "Cipla Limited": ["CIPLA"],
        "Divi's Laboratories Limited": ["DIVIS"],
        "Apollo Hospitals Enterprise Limited": ["APOLLO"],

        "UltraTech Cement Limited": ["ULTRATECH"],
        "Grasim Industries Limited": ["GRASIM"],
        "Shree Cement Limited": ["SHREECEM"],
        "Ambuja Cements Limited": ["AMBUJA"],
        "ACC Limited": ["ACC"],

        "ITC Limited": ["ITC"],
        "Nestle India Limited": ["NESTLE"],
        "Britannia Industries Limited": ["BRITANNIA"],
        "Godrej Consumer Products Limited": ["GODREJ"],
        "Dabur India Limited": ["DABUR"],

        "Zomato Limited": ["ZOMATO"],
        "FSN E-Commerce Ventures Limited": ["NYKAA"],
        "One 97 Communications Limited": ["PAYTM"],
        "PB Fintech Limited": ["POLICYBAZAAR"],
    }

    @classmethod
    def generate_aliases(
        cls,
        company_name: str,
    ) -> list[str]:

        aliases: Set[str] = set()

        if not company_name:
            return []

        company_name = company_name.strip()

        # Full company name
        aliases.add(company_name)

        words = company_name.split()

        # Remove company suffixes
        cleaned_words = [
            word
            for word in words
            if word.lower().strip(".,")
            not in cls.COMPANY_SUFFIXES
        ]

        if cleaned_words:

            cleaned_name = " ".join(cleaned_words)

            # Company name without Limited/Ltd
            aliases.add(cleaned_name)

            # First word
            first_word = cleaned_words[0]

            if (
                len(first_word) >= 4
                and not any(char.isdigit() for char in first_word)
                and first_word.lower() not in cls.GENERIC_FIRST_WORDS
            ):
                aliases.add(first_word)

        # Manual aliases
        manual_aliases = cls.MANUAL_ALIASES.get(
            company_name,
            [],
        )

        for alias in manual_aliases:
            aliases.add(alias)

        # Remove empty values
        aliases = {
            alias.strip()
            for alias in aliases
            if alias and alias.strip()
        }

        # Sort by length descending
        # (longer aliases match first later)
        return sorted(
            aliases,
            key=len,
            reverse=True,
        )