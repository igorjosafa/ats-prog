from ats_prog import incluir_matriculas_manualmente
import pandas as pd
from unittest.mock import patch
from io import StringIO

@patch("sys.stdin", StringIO("12345;23412"))
def test_incluir_matriculas_manualmente():
    matriculas_teste = pd.Series([24251, 34357, 46578])
    ret = incluir_matriculas_manualmente(matriculas_teste, 'ATS')
    expected = pd.Series([24251, 34357, 46578, 12345, 23412])
    assert ret.reset_index(drop=True).equals(expected.reset_index(drop=True))
