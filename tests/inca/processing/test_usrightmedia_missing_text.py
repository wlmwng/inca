import pytest
from inca.core.processor_class import Processer
from inca.processing.usrightmedia_missing_text_processing import (
    missing_text_americanrenaissance,
    missing_text_breitbart,
    missing_text_dailycaller,
    missing_text_dailystormer,
    missing_text_foxnews,
    missing_text_gatewaypundit,
    missing_text_infowars,
    missing_text_newsmax,
    missing_text_oneamericanews,
    missing_text_rushlimbaugh,
    missing_text_seanhannity,
    missing_text_vdare,
    missing_text_washingtonexaminer,
)


@pytest.fixture
def text_extra_spaces_only():
    yield "      "


@pytest.fixture
def text_extra_spaces_with_content():
    yield " A document with text inside of it and extra    spaces .  "


class TestMissingTextAmericanRenaissance(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_americanrenaissance(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_americanrenaissance(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False

    def test_generic(self):
        """Check an outlet-specific generic string"""
        text_generic = "AmRen is America's foremost white advocacy publication. To keep up with our latest, follow us on Telegram Gab , and BitChute"
        processor = missing_text_americanrenaissance(Processer)
        result = processor.process(text_generic)
        assert result is True


class TestMissingTextBreitbart(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_breitbart(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_breitbart(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False


class TestMissingTextDailyCaller(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_dailycaller(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_dailycaller(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False


class TestMissingTextDailyStormer(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_dailystormer(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_dailystormer(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False

    def test_generic(self):
        """Check an outlet-specific generic string"""
        text_generic = "We here at the Daily Stormer are opposed to violence. We seek revolution through the education of the masses. When the information is available to the people, systemic change will be inevitable and unavoidable.\nAnyone suggesting or promoting violence in the comments section will be immediately banned, permanently."
        processor = missing_text_dailystormer(Processer)
        result = processor.process(text_generic)
        assert result is True


class TestMissingTextFoxNews(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_foxnews(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_foxnews(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False

    def test_generic(self):
        """Check an outlet-specific generic string"""
        text_generic = (
            "By using this site, you agree to our Privacy Policy and our Terms of Use"
        )
        processor = missing_text_foxnews(Processer)
        result = processor.process(text_generic)
        assert result is True


class TestMissingTextGatewayPundit(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_gatewaypundit(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_gatewaypundit(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False

    def test_generic(self):
        """Check an outlet-specific generic string"""
        text_generic = "The page you are looking for no longer exists. Perhaps you can return back to the site's homepage and see if you can find what you are looking for. Or, you can try finding it with the information below."
        processor = missing_text_gatewaypundit(Processer)
        result = processor.process(text_generic)
        assert result is True


class TestMissingTextInfoWars(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_infowars(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_infowars(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False

    def test_generic(self):
        """Check an outlet-specific generic string"""
        text_generic = "Keep up to date with our latest:\nHave an important tip? Let us know. Email us here."
        processor = missing_text_infowars(Processer)
        result = processor.process(text_generic)
        assert result is True


class TestMissingTextNewsmax(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_newsmax(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_newsmax(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False


class TestMissingTextOneAmericaNews(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_oneamericanews(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_oneamericanews(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False

    def test_generic(self):
        """Check an outlet-specific generic string"""
        text_generic = "It seems we can’t find what you’re looking for. Perhaps searching can help.\nSearch for:"
        processor = missing_text_oneamericanews(Processer)
        result = processor.process(text_generic)
        assert result is True

    def test_unrelated_preview(self):
        """Check an outlet-specific generic string"""
        text_preview = "this is a short document which contains the read more preview button\nRead More"
        processor = missing_text_oneamericanews(Processer)
        result = processor.process(text_preview)
        assert result is True


class TestMissingTextRushLimbaugh(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_rushlimbaugh(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_rushlimbaugh(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False

    def test_date_only(self):
        """Check an outlet-specific generic string"""
        text_date_only = "Jun 23, 2018"
        processor = missing_text_rushlimbaugh(Processer)
        result = processor.process(text_date_only)
        assert result is True


class TestMissingTextSeanHannity(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_seanhannity(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_seanhannity(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False


class TestMissingTextVdare(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_vdare(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_vdare(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False


class TestMissingTextWashingtonExaminer(object):
    def test_extra_spaces_only(self, text_extra_spaces_only):
        """Check an empty string"""
        processor = missing_text_washingtonexaminer(Processer)
        result = processor.process(text_extra_spaces_only)
        assert result is True

    def test_extra_spaces_with_content(self, text_extra_spaces_with_content):
        """Check a non-empty string"""
        processor = missing_text_washingtonexaminer(Processer)
        result = processor.process(text_extra_spaces_with_content)
        assert result is False
