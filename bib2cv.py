import biblib.bib
import biblib.messages
import biblib.algo
import argparse
import sys
import re
import calendar

CITATION_STYLE = 'ieee'

BIBTEX_ENTRY_TYPE_FIELDS = {
    'article'       : ['author','title','journal','volume','number','pages','year','doi'],
    'inproceedings' : ['author','title','booktitle','year','pages','doi'],
    'phdthesis'     : ['author','title','school','address','year'],
    'mastersthesis' : ['author','title','school','address','year'],
}

PUBLICATION_TYPES = [       # print in order
    {'name':'journals', 'display_name':'Journals', 'entry_types':['article',]},
    {'name':'conferences', 'display_name':'Conferences', 'entry_types':['inproceedings','conference',]},
    {'name':'thesis', 'display_name':'Theses and dissertations', 'entry_types':['phdthesis','mastersthesis',]},
] 

parsed_entry_bins = {
        'article'       : [],
        'inproceedings' : [],
        'conference'    : [],
        'phdthesis'     : [],
        'mastersthesis' : [],
    }


def parse(*files, user=None):
    # parse files, put entries into bins
    for bibfile in files:
        with open(bibfile, 'r') as fp:
            try:
                # Load databases
                db = biblib.bib.Parser().parse(fp).get_entries()

                # Resolve cross-references
                db = biblib.bib.resolve_crossrefs(db)
       
                # Print entries
                recoverer = biblib.messages.InputErrorRecoverer()
                for ent in db.values():
                    with recoverer:
                        parsed_entry_bins[ent.typ].append(ent)
                recoverer.reraise()
            except biblib.messages.InputError:
                print("Input error!")
                sys.exit(1)

    # print publication types in order
    for pt in PUBLICATION_TYPES:
        print('\\subsubsection{'+pt['display_name']+'}\\label{'+pt['name']+'}')
        print('\\begin{enumerate}')

        for et in pt['entry_types']:
            for ent in parsed_entry_bins[et]:
                print_entry(CITATION_STYLE, ent, user)

        print('\\end{enumerate}')

def print_entry(style, ent, user):
    last_name = ''
    first_name = '' 
    if user:
        user = user.split(',')
        if len(user) == 1:
            user.append('')
        last_name = user[0]
        first_name = user[1]

    citation = ''
    fields = []
    for idx, field in enumerate(BIBTEX_ENTRY_TYPE_FIELDS[ent.typ]):
        if field == 'author' and field in ent:
            authors = []
            for author in ent.authors():
                name = biblib.algo.tex_to_unicode(ieee_name(author),
                    pos=ent.field_pos['author'])
                if (author.first.lower()==first_name.lower() 
                        and author.last.lower()==last_name.lower()):
                    name = '\\textbf{'+name+'}'
                authors.append(name)
            if len(authors) == 0:
                author = None
            elif len(authors) == 1:
                author = authors[0]
            else:
                author = ', '.join(authors[:-1])
                if len(authors) > 2:
                    author += ','
                if ent.authors()[-1].is_others():
                    author += ' et al.'
                else:
                    author += ' and ' + authors[-1]
            author += ', '
            citation += author

        if field == 'title' and field in ent:
            title = biblib.algo.tex_to_unicode(biblib.algo.title_case(
                ent['title'], pos=ent.field_pos['title']))
            if re.search(r"[?.!]$",ent['title']) is None:
                title += ','
            title = '\"'+title+'\" '
            citation += title

        if field == 'booktitle' and field in ent:
            conf = ent['booktitle']
            conf.replace('&', '\&')
            conf = 'in \\textit{'+conf+'}'
            fields.append(conf)
 
        if field == 'journal' and field in ent:
            journal = ent['journal']
            journal.replace('&', '\&')
            journal = '\\textit{'+journal+'}'
            fields.append(journal)

        if field == 'volume' and field in ent:
            vol = ent['volume']
            vol = 'vol. '+vol
            fields.append(vol)
            
        if field == 'number' and field in ent:
            num = ent['number']
            num = 'no. '+num
            fields.append(num)

        if field == 'pages' and field in ent:
            pp = ent['pages']
            pp = 'pp. '+pp
            fields.append(pp)

        if field == 'year' and field in ent:
            year = ent['year']
            if 'month' in ent:
                year = calendar.month_abbr[int(ent['month'])]+'. '+year
            fields.append(year)

        if field == 'doi' and field in ent:
            doi = ent['doi']
            doi = 'doi: \\href{http://dx.doi.org/'+doi+'}{'+doi+'}'
            fields.append(doi)

        if field == 'school' and field in ent:
            school = ent['school']
            school.replace('&', '\&')
            fields.append(school)

        if field == 'address' and field in ent:
            address = ent['address']
            address.replace('&', '\&')
            fields.append(address)

    citation += ', '.join(fields)
    print('\\item ' + citation)


def ieee_name(name):
    first = '' if not name.first else name.first[0]+'. '
    von = '' if not name.von else name.von[0]+'. '
    last = name.last
    jr = '' if not name.jr else ', '+name.jr
    return first+von+last+jr


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-u', '--user', help='the name that need textbf')
    arg_parser.add_argument('bib', nargs='+', help='.bib file(s) to process')
    args = arg_parser.parse_args()
    parse(*args.bib, user=args.user)
