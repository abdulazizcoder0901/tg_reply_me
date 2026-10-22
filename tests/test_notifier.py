from datetime import datetime, timezone
from types import SimpleNamespace

import notifier


def _build(**overrides):
    params = dict(
        kind=notifier.KIND_MENTION,
        chat_title="Dasturchilar",
        chat_username="dev_uz",
        sender_name="Ali Valiyev",
        sender_username="ali",
        sender_id=12345,
        date=datetime(2026, 10, 22, 7, 30, 15, tzinfo=timezone.utc),
        tz="Asia/Tashkent",
        text="Salom @me",
    )
    params.update(overrides)
    return notifier.build_notification(**params)


def test_public_chat_link():
    assert notifier.message_link(-1001234, "dev_uz", 55) == "https://t.me/dev_uz/55"


def test_private_supergroup_link():
    assert notifier.message_link(-1001234567, None, 55) == "https://t.me/c/1234567/55"


def test_basic_group_has_no_link():
    assert notifier.message_link(-4567, None, 55) is None


def test_mention_contains_all_fields():
    text = _build()
    assert "Sizni belgilashdi" in text
    assert "Dasturchilar" in text and "@dev_uz" in text
    assert 'href="tg://user?id=12345"' in text and "@ali" in text
    assert "22.10.2026 12:30:15" in text  # UTC+5
    assert "Salom @me" in text


def test_reply_shows_quoted_message():
    text = _build(kind=notifier.KIND_REPLY, replied_text="Mening xabarim")
    assert "Xabaringizga javob berishdi" in text
    assert "Mening xabarim" in text


def test_html_is_escaped():
    text = _build(text="<b>x</b> & y", chat_title="A<B>")
    assert "&lt;b&gt;x&lt;/b&gt; &amp; y" in text
    assert "A&lt;B&gt;" in text


def test_long_text_is_shortened():
    text = _build(text="a" * 5000)
    assert "a" * notifier.MAX_TEXT not in text
    assert "…" in text


def test_media_label_and_empty_text():
    msg = SimpleNamespace(photo=object(), document=None)
    label = notifier.media_label(msg)
    assert label == "🖼 Rasm"
    text = _build(text="", media=label)
    assert "[🖼 Rasm]" in text


def test_no_text_no_media():
    assert "(matn yo'q)" in _build(text="")
