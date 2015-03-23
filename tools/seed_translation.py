from translate import Translator
import polib
import os

po_files_dir = '/home/gonzalo/sugar-devel/honey/help/help-activity/translated_po/es'

files = os.listdir(po_files_dir)

translator= Translator(to_lang="es")

for po_file_name in files:
    print "TRANSLATE %s" % po_file_name
    po = polib.pofile(os.path.join(po_files_dir, po_file_name))
    for entry in po:
        if entry.msgstr == '':
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
