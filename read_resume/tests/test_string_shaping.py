import pytest
from utils.string_shaping import clean_text,remove_duplicate_lines


# 正常系-----------------------------------------------------
# clean_text
def test_remove_nan_and_empty_lines():
    input_text  = "NaN\nHello\n  \nnan\nWorld\n"
    output_text = "Hello\nWorld"

    assert clean_text(input_text) == output_text



# remove_duplicate_lines
def test_duplicate_string() -> str:
    input_text  = "foge\nhello\nhello\nhello\nkon"
    output_text = "foge\nhello\nhello\nkon"

    result = remove_duplicate_lines(input_text)
    print(result)
    assert result == output_text

# 異常系-----------------------------------------------------

