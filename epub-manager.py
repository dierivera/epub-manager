import zipfile
from lxml import etree

#Library that gets the content from an epub file
#Creates an object type epub (here's the code) with the info about it

class epub:
    def __init__(self, identifier, author, language, title, date):
        self.identifier = identifier
        self.author = author
        self.language = language  
        self.title = title
        self.date = date
    def imprimir(self): #print like function
        print(self.author +" - "+ self.title)
        
def get_epub_info(fname):
    ns = {
        'n':'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg':'http://www.idpf.org/2007/opf',
        'dc':'http://purl.org/dc/elements/1.1/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]

    # repackage the data
    title = p.xpath('dc:%s/text()'%('title'),namespaces=ns)[0]
    language = p.xpath('dc:%s/text()'%('language'),namespaces=ns)[0]
    creator = p.xpath('dc:%s/text()'%('creator'),namespaces=ns)[0]
    date = p.xpath('dc:%s/text()'%('date'),namespaces=ns)[0]
    identifier = p.xpath('dc:%s/text()'%('identifier'),namespaces=ns)[0]
    #build the epub object (named book)
    book = epub(identifier, creator, language, title, date);

    return book.imprimir()



example = 'El Laberinto de los Espiritus - Carlos Ruiz Zafon.epub' #epub file route
get_epub_info(example) #running this when executing the code
