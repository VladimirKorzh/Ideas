# -*- coding: utf-8 -*-
import csv, sqlite3
import os
import nltk
import string
from nltk.stem.wordnet import WordNetLemmatizer


def replace(con, column, old_value, new_value):
    if con != None:
        cur = con.cursor()

        table = 'gimlet_csv'
        sqlstr = 'UPDATE ' + table + ' SET '
        sqlstr += column + ' = REPLACE(' + column + ', "' + old_value + '", "' + new_value + '");'
        cur.execute(sqlstr)







class QueryBuilder():
    def __init__(self):
        self.columns = ['*']
        self.table = 'gimlet_csv'
        self.conditions = []
        self.limit = 10
        self.console = False
        self.show = True
        self.last_result = None

    def set_columns(self,columns):
        self.columns = []
        self.columns = columns

    def set_condition(self,column, like):
        if (column,like) not in self.conditions:
            self.conditions.append((column, like))

    def log(self):
        print 'Columns: ',
        print self.columns
        print 'Conditions: ',
        print self.conditions
        print 'Limit: '+str(self.limit)

    def display(self, what):
        index_list = []
        ret = []
        for each in what:
            index_list.append(self.columns.index(each))

        if self.last_result:
            for each in self.last_result:
                for index in index_list:
                    if self.show == True: print each[index]
                    if self.show == False: ret.append(each[index])

        if self.show == False:
            return ret



    def execute(self,con):
        cur = None
        rows = None
        if con != None:
            cur = con.cursor()

        columns = self.columns[:]
        conditions = self.conditions[::-1]

        query = 'SELECT'
        if len(columns) >= 1:
            query += ' ' + columns.pop(0)

            while len(columns):
                each = columns.pop(0)
                query += ', ' + each

        query += ' FROM ' + self.table

        if len(conditions) >= 1:
            query += ' WHERE'
            while len(conditions):
                each = conditions.pop()
                query += ' ' + each[0] + " LIKE '%" + each[1] + "%'"


                #each = conditions.pop()
                #query += ' AND ' + each[0] + " LIKE '%" + each[1] + "%'"

        if self.limit != 0:
            query += ' LIMIT ' + str(self.limit)

        if cur != None:
            cur.execute(query)
            rows = cur.fetchall()
            self.last_result = rows

        if self.show:
            self.log()

        if con == None:
            print query

        return rows

# <headingcell level=1>

# Query builder unit testing

# <codecell>

"""
q = QueryBuilder()
q.set_columns( ['Email', 'Answer'] )
q.set_condition('Answer', 'null')
q.limit = 10
q.execute(None)

q.set_columns( ['Question','Email','Answer','Format'] )
q.execute(None)


q = None                                      # Clear previous query
q = QueryBuilder()                    # Create a new custom query
q.set_columns(['Question'])                   # we are interested in question and email columns
q.show = False                                # not displaying the result of this query on screen
q.limit = 0                                   # allows us to take out the result limitations
print q.conditions
q.execute(None)

"""


# <headingcell level=1>

# Data Manager class

# <codecell>

lmtzr = WordNetLemmatizer()		
def lemmatize_question(text):
	return 	' '.join([ lmtzr.lemmatize(each) for each in nltk.word_tokenize(text) ])
		
class DataManager():
    def import_data(self,cwd):
        data = {}   # raw data that was read from csv file

        # get current directory path and find all csv files in it
        csvfiles = [ f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd,f)) and f.endswith('.csv') ]

        # read the data from csv files
        print '\nReading input data files from', cwd
        for each in csvfiles:
            print 'Found',each,'...',
            data[each] = []

            with open(os.path.join(cwd, each), 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')

                for each_row in reader:
                    data[each].append(each_row)
                print len(data[each]),' records imported'

        return data
	


    def get_python_columns(self,data):
        # find all possible columns
        columns = []
        columns.append('filename')
        for each in data:
          for each_column in data[each][0]:
            # convert the names into possible and acceptable database table-row names
            each_column = each_column.replace(' ', '_').replace('(', '').replace(')', '').replace('\xef\xbb\xbf','').lower()
            if each_column not in columns:
                columns.append(each_column)
        return columns

    def get_db_columns(self, con):
        con.row_factory = sqlite3.Row
        cursor = con.execute('select * from gimlet_csv')
        row = cursor.fetchone()
        names = row.keys()
        return names

    def save_data_to_db(self,data):
        # load lemmatizer for singular forms of words


        # prepare the database
        con = sqlite3.connect(":memory:")
        con.text_factory = str # FIX to switch away from unicode strings

        columns = self.get_python_columns(data)

        print '\nCreating database layout...'
        cur = con.cursor()
        try:
            prep_statement = "CREATE TABLE gimlet_csv ("+','.join(columns)+");"
            #print prep_statement
            cur.execute(prep_statement)
            print 'Table created.'
        except sqlite3.OperationalError:
            print 'Table already exists.'


        print '\nInserting data into database...'
        q_values = ', '.join(['?' for i in range(1,len(columns)+1)])
        prep_statement = "INSERT INTO gimlet_csv ("+','.join(columns)+") VALUES ("+q_values+");"
        #print prep_statement
        for each in data:
            for each_row in data[each][1:]:
                values = []
                values.append(each)
                for each_val in each_row:
                    if each_val =='':
                      each_val = 'null'
                    values.append(lemmatize_question(each_val.lower()))

                cur.execute(prep_statement, values)
        con.commit()
        print 'Done.'
        return con


class DataAnalyzer():
    def get_text(self, rows):
        full_text = ''
        for row in rows:
          # prepare the question string by converting it into lowercase and stripping out all of the stopwords
          question = row[0].lower()
          question = "".join(l for l in question if l not in string.punctuation)
          for word in question.split():
            if word not in nltk.corpus.stopwords.words('english'):
                if str(word) != str('null'):
                    full_text += ' ' + word

        return full_text


    def db_get_full_text(self, con):
        print 'Analyzing questions text-body... Done.'
        cur = con.cursor()
        cur.execute("SELECT Question FROM gimlet_csv")
        rows = cur.fetchall()
        return self.get_text(rows)



    def get_most_frequent_words(self, text, amount=50,draw=True):
        fd = nltk.FreqDist()

        for word in text.split():
          fd.inc(word)

        return fd.items()[:amount]

    def pie_chart(self, info):
        labels = [l[0] for l in info]
        sizes = [l[1] for l in info]
        colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

        rcParams['figure.figsize'] = 10, 10

        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.show()

    def get(self, con):
        cur = con.cursor()
        cur.execute("SELECT * FROM gimlet_csv WHERE Question='null'")
        full_text = ''
        rows = cur.fetchall()

        for row in rows:
          print row

# <codecell>

#def percentage(part, whole):
  #return 100 * float(part)/float(whole)

