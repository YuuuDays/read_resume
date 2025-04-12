import pytest
from utils.string_shaping import clean_text


# 正常系-----------------------------------------------------
def test_remove_nan_and_empty_lines():
    input_text  = "NaN\nHello\n  \nnan\nWorld\n"
    output_text = "Hello\nWorld"

    assert clean_text(input_text) == output_text



# 異常系-----------------------------------------------------

