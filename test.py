from googletrans import Translator

translator = Translator()
x = translator.translate('please acknowledge me', dest='hindi')
print(x)