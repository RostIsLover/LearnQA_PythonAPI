class TestPhraseLength:
    def test_phrase_length(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, "Phrase is not shorter than 15 symbols"
