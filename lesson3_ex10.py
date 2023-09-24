class TestSetPhraseIsLessThan15Symbols:
    def test_set_phrase_is_less_than_15_symbols(self):
        phrase = input("Set a phrase: ")
        phrase_length = len(phrase)

        assert phrase_length < 15, f"The set phrase '{phrase}' is equal or more than 15 symbols"
