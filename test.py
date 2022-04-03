from hmac import trans_36
from googletrans import Translator
import googletrans

t=Translator()

print(googletrans.LANGUAGES)

print(t.translate("hello", dest='ps'))