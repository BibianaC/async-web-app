from async_web_app import count_words, get_most_common_words


def test_count_words():
    text = "hello world hello world hello"
    counter = count_words(text)
    assert counter == {'hello': 3, 'world': 2}


def test_count_words_when_exception():
    text = "hello world hello world hello u 1 2 3"
    counter = count_words(text)
    assert counter == {'hello': 3, 'world': 2}


def test_get_most_common_words():
    text_list = ['s%0d' % i for i in range(110)]
    text_str = ' '.join(text_list)
    counter = count_words(text_str)
    assert len(counter) == 110

    most_common = get_most_common_words(counter)
    most_common_split = most_common.split()
    assert len(most_common_split) == 100
