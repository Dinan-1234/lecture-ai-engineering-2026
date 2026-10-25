from types import SimpleNamespace
from unittest.mock import patch

from app.ask import ask


def test_ask_prints_token_usage(capsys):
    fake_response = SimpleNamespace(
        text="これはテストです。",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=7),
    )
    fake_client = SimpleNamespace(
        models=SimpleNamespace(generate_content=lambda **kwargs: fake_response)
    )

    with patch("app.ask.genai.Client", return_value=fake_client):
        with patch("app.ask.get_api_key", return_value="fake-key"):
            result = ask("テスト")

    assert result == "これはテストです。"
    output = capsys.readouterr().out
    assert "入力トークン数: 12" in output
    assert "出力トークン数: 7" in output
