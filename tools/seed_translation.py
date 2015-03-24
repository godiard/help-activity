from translate import Translator
import polib
import os

language_code = 'es'

po_files_dir = './translated_po/%s' % language_code

files = os.listdir(po_files_dir)
#files = ['abacus.po']
translate_all = True

translator= Translator(to_lang=language_code)

for po_file_name in files:
    print "TRANSLATE %s" % po_file_name
    po = polib.pofile(os.path.join(po_files_dir, po_file_name))
    for entry in po:
        if translate_all or entry.msgstr == '':
            print entry.msgid
            sentences = entry.msgid.split('.')
            translated_sentences = []
            for sentence in sentences:
                try:
                    translated_sentences.append(translator.translate(sentence))
                except:
                    print "ERROR TRANSLATING SENTENCE '%s'" % sentence
            translation = '. '.join(translated_sentences)
            print translation
            print "-" * 40
            entry.msgstr = translation.strip()
    po.save(os.path.join(po_files_dir, po_file_name))
